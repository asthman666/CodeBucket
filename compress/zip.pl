#!/usr/bin/perl
use strict;
use warnings;
use Path::Tiny;
use Getopt::Long;

my ($input_dir, $output_dir, $password);
GetOptions( "input_dir=s" => \$input_dir,
	    "output_dir=s" => \$output_dir,
	    "password=s" => \$password,
    );


if ( !$input_dir ) {
    usage();
    exit 0;
}

my $dir = path($input_dir);
foreach my $child ( $dir->children() ) {
    if ( $child->is_dir ) {
	my $dir_name = $child->basename;
	next if $dir_name =~ /^\./;
	
	chdir($input_dir);

	my $cmd = "/usr/bin/zip -r -P $password $dir_name.zip $dir_name/\n";
	#print $cmd, "\n";
	system($cmd);
    }
}
