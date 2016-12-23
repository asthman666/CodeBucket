use PDF::API2;
use utf8;
my $str = "中国";

# Create a blank PDF file
$pdf = PDF::API2->new();

$cft=$pdf->cjkfont('Song');

$page = $pdf->page();

# Add some text to the page
$text = $page->text();
$text->font($cft, 20);
$text->translate(200, 200);
$text->text($str);

# Save the PDF
$pdf->saveas('./new.pdf');

