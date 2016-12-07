#!/usr/bin/perl
use strict;
use warnings;
use Selenium::Chrome;

my $driver = Selenium::Chrome->new(proxy => {proxyType => 'direct'});
my $url = "http://www.baidu.com";
$driver->get($url);
sleep 10;
$driver->shutdown_binary;




