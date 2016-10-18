<?php

$input  = "Warped text!";
$width  = 200;
$height = 200;

// Allocate initial image with a solid white background.
$original = imagecreatetruecolor($width, $height);
imagefill($original, 0, 0, imagecolorallocate($original, 255, 255, 255));

// Write something onto the original image:
imagestring($original, 5, 0, 0, $input, imagecolorallocate($original, 0, 0, 0));

// A target image, we'll warp the original and render onto this canvas.
$warped = imagecreatetruecolor($width, $height);
imagefill($warped, 0, 0, imagecolorallocate($warped, 255, 255, 255));

// Iteratore over each pixel and warp the coordinates
for($x = 0; $x < $width; ++$x) {
	for($y = 0; $y < $height; ++$y) {
		
		// Sample color of the original image
		$components = imagecolorsforindex($original, imagecolorat($original, $x, $y));

		// Create a new color for the warped image
		$color = imagecolorallocate($warped, $components["red"], $components["green"], $components["blue"]);

		// Warp the target X / Y coordinates
		$warpX = $x;
		$warpY = $y + sin($x / 30) * 10;

		imagesetpixel($warped, $warpX, $warpY, $color);
	}
}


// Output the image
header('Content-type: image/png');
imagepng($warped);

// Destroy allocated resources
imagedestroy($warped);
imagedestroy($original);

