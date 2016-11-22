#!/usr/bin/perl
use strict;
use Mail::IMAPClient;
use Data::Dumper;
use Encode::HanExtra;
use MIME::Parser;
use MIME::Base64;
use Getopt::Long;

my ($server, $user, $password);
GetOptions( "server=s" => \$server,
	    "user=s" => \$user,
	    "password=s" => \$password,
	  );

my $imap = Mail::IMAPClient->new(
  Ignoresizeerrors => 1,
  Server   => $server, # imap.qq.com
  User     => $user,
  Password => $password,
  Ssl      => 1,
  Uid      => 1,
);

my $parser = MIME::Parser->new;

my $folders = $imap->folders;
 
foreach ( @$folders ) {
    next if $_ ne 'INBOX';
    $imap->select( $_ );
    my @msgs = $imap->messages;    
    foreach my $msgid ( @msgs ) {
	print "get msgid: $msgid", "\n";
	my $string = $imap->message_string($msgid);
	if ( length($string) == 0 ) {
            print "List folders error: ", $imap->LastError, "\n";
	    next;
	}
	
	my $entity = $parser->parse_data($string);
	my $is_multipart = $entity->is_multipart;
	my $header = $entity->head;
	my $date = $header->get("date");
	my @from = $header->get_all("From");
	my @to = $header->get_all("To");
	my $msg_id = $header->get("message-id");
	my $mime_type = $header->mime_type;
	my $mime_encoding = $header->mime_encoding;
	my $file_name = $header->recommended_filename;

	print "is_multipart: $is_multipart\n";
	print "Date: $date";
	print "From: ". Dumper(\@from);
	print "To: " . Dumper(\@to);
	print "Message-id:  $msg_id";
	print "mime_type: $mime_type\n";
	print "mime_encoding: $mime_encoding\n";
	print "file_name: $file_name\n";

	my $subject = $header->get("subject");
	$subject = Encode::decode('MIME-Header', $subject);
	print "Subject: $subject\n";

	my $num_parts  = $entity->parts;
	print "num parts: $num_parts\n";

	if ( $num_parts ) {
	    foreach ( 0..$num_parts ) {
		print "get part: $_\n";
		my $part = $entity->parts($_);
		next unless $part;
		my $content = $part->stringify_body;
		$content = decode_base64($content);
		$content = Encode::decode('gbk', $content);
		print "Content: $content\n";
	    }
	}
    }
}

