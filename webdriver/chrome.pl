#!/usr/bin/perl
use strict;
use warnings;
use Selenium::Chrome;

my $driver = Selenium::Chrome->new(proxy => {proxyType => 'direct'});
my $url = "http://www.baidu.com";
$driver->get($url);
my $current_url = $driver->get_current_url;
print "current_url: $current_url", "\n";
sleep 5;
$driver->shutdown_binary;




