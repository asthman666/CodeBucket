#!/usr/bin/perl
use strict;
use Mail::IMAPClient;
use Data::Dumper;
use MIME::Tools;
use MIME::Parser;
use Encode;
use Encode::Guess qw/gbk cp936/;
use Encode::HanExtra;
use DateTime;
use Getopt::Long;
use Time::ParseDate;

binmode STDOUT, ":encoding(UTF-8)";

my ($server, $user, $password, $output_dir, $test_email_num, $date, $today, $test_msgid, $debug, $help);
GetOptions( "server=s" => \$server,
	    "user=s" => \$user,
	    "password=s" => \$password,
            "output_dir=s" => \$output_dir,
            "test_email_num=i" => \$test_email_num,
            "test_msgid=i" => \$test_msgid,
            "debug+" => \$debug,
            "help!" => \$help,
            "today!" => \$today,
            "date=s" => \$date,
    );

if ( $help || (!$server || !$user || !$password) ) {
    usage();
    exit 0;
}

my $imap = Mail::IMAPClient->new(
  Ignoresizeerrors => 1,
  Server   => $server, # imap.qq.com
  User     => $user,
  Password => $password,
  Ssl      => 1,
  Uid      => 1,
);

unless ($imap) {
    print "Cannot connect to $server as $user: $@\n";
    exit 0;
}

if ( $debug && $debug == 2 ) {
    MIME::Tools->debugging(1);
    MIME::Tools->quiet(0);
}

my $parser = MIME::Parser->new;
$output_dir ||= "/tmp";
$parser->output_dir($output_dir);

my $time;
if ( $today ) {
    $time = DateTime->today->epoch();
} elsif ( $date ) {
    $time = parsedate($date)
}

my $folders = $imap->folders;

unless ( $folders ) {
    print "Could not list folders: $@\n";
    exit 0;
}
 
my $index;
foreach ( @$folders ) {
    next if $_ ne 'INBOX';
    $imap->select( $_ );

    my @msgs;
    if ( $time ) {
        @msgs = $imap->since($time);
    } else {
        @msgs = $imap->messages;    
    }

    foreach my $msgid ( @msgs ) {
        next if $test_msgid && $test_msgid != $msgid;
	print "===================get msgid: $msgid===================", "\n";
	my $string = $imap->message_string($msgid);
	if ( length($string) == 0 ) {
            print "List folders error: ", $imap->LastError, "\n";
	    next;
	}

        my $subject = $imap->subject($msgid);
	$subject = Encode::decode('MIME-Header', $subject);
	print "Subject: $subject\n";
        
        $parser->output_prefix("msg-$msgid"); # change the output file prefix to distinguish the relation between email and the output file 

	my $entity = $parser->parse_data($string);
	#$entity->dump_skeleton; # for debugging, debug the entity

	my $is_multipart = $entity->is_multipart;
	my $header = $entity->head;
	my $date = $header->get("date");
	my @from = $header->get_all("From");
	my @to = $header->get_all("To");
	my $msg_id = $header->get("message-id");
	my $mime_type = $header->mime_type;
	my $mime_encoding = $header->mime_encoding;

	print "is_multipart: $is_multipart\n" if $debug == 1;
	print "Date: $date\n";
	print "From: ". Dumper(\@from) if $debug;
	print "To: " . Dumper(\@to) if $debug;
	print "Message-id:  $msg_id" if $debug;
	print "mime_type: $mime_type\n" if $debug;
        print "mime_encoding: $mime_encoding\n" if $debug;

	#my $subject = $header->get("subject");
	#$subject = Encode::decode('MIME-Header', $subject);
	#print "Subject: $subject";

	my $num_parts  = $entity->parts;
	print "num parts: $num_parts\n" if $debug;

        my $data = find_entity_text($entity);
        #print "data: $data\n" if $debug;
        if ( $data ) {
            $data = decode("Guess", $data);
            print "Content: $data\n";
        }

        $index++;
	last if $test_email_num && $index >= $test_email_num;
    }
}

sub find_entity_text {
    my $entity = shift;
    
    if ( $entity->mime_type eq 'text/plain' && $entity->bodyhandle ) {
        #print $entity->bodyhandle->path, "\n" if $debug;
        #print $entity->bodyhandle->as_string, "\n" if $debug;
        return $entity->bodyhandle->as_string;
    } else {
        for (0..$entity->parts-1) {
            my $part = $entity->parts($_);
            my $data = find_entity_text($part);
            return $data if $data;
        }
    }
    return;
}

sub usage {
    print "Usage: perl imap.pl --server imap.qq.com --user user_name --password password --date '2016-11-24'\n";
}
