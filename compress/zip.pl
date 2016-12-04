#!/usr/bin/perl
use strict;
use warnings;
use Path::Tiny;
use Getopt::Long;
use Data::Dumper;

my ($input_dir, $zip_dir, $output_dir, $password, $help, $execute);
GetOptions( "input_dir=s" => \$input_dir,
	    "zip_dir=s" => \$zip_dir,   # the dir need to be ziped, default all dirs below input_dir 
	    "output_dir=s" => \$output_dir,
	    "password=s" => \$password,
	    "help|?" => sub { usage() },
	    "execute!" => \$execute,
    );

if ( !$input_dir || !$password ) {
    usage();
}

my $idir = path($input_dir);

my @zip_files;

if ( $output_dir ) {
    my $odir = path($output_dir);
    foreach ( $odir->children(qr/\.zip/) ) {
	push @zip_files, $_->basename;
    }
}

foreach my $child ( $idir->children() ) {
    if ( $child->is_dir ) {
	my $dir_name = $child->basename;
	next if $dir_name =~ /^\./;
	next if $zip_dir && $zip_dir ne $dir_name;
	next if ( grep {"${dir_name}.zip" eq $_} @zip_files );

	chdir($input_dir);

	$output_dir =~ s{/$}{};
	my $cmd = "/usr/bin/zip -r -P $password '${output_dir}/${dir_name}.zip' '$dir_name'/";
	print $cmd, "\n";
	system($cmd) if $execute;
    }
}

sub usage {
    print "Usage: perl zip.pl --output_dir /media/asthman/我的移动硬盘/photo --input_dir /media/asthman/000F7AEF000C7375/photo --password xxx\n";
    exit 0;
}
