#!/usr/bin/php
<?php

if (!function_exists('stats_standard_deviation')) {
    /**
     * This user-land implementation follows the implementation quite strictly;
     * it does not attempt to improve the code or algorithm in any way. It will
     * raise a warning if you have fewer than 2 values in your array, just like
     * the extension does (although as an E_USER_WARNING, not E_WARNING).
     *
     * @param array $a
     * @param bool $sample [optional] Defaults to false
     * @return float|bool The standard deviation or false on error.
     */
    function stats_standard_deviation(array $a, $sample = false) {
        $n = count($a);
        if ($n === 0) {
            trigger_error("The array has zero elements", E_USER_WARNING);
            return false;
        }
        if ($sample && $n === 1) {
            trigger_error("The array has only 1 element", E_USER_WARNING);
            return false;
        }
        $mean = array_sum($a) / $n;
        $carry = 0.0;
        foreach ($a as $val) {
            $d = ((double) $val) - $mean;
            $carry += $d * $d;
        };
        if ($sample) {
           --$n;
        }
        return sqrt($carry / $n);
    }
}

$path = $argv[1];

$files = scandir($path);

$widths = array();
$heights = array();

foreach($files as $file) {
	
	if(strlen($file) > 0 && $file[0] != ".") {	
		list($width, $height, $type, $attr) = getimagesize($path . "/" . $file);
	
		$widths[] = $width;
		$heights[] = $height;
	}
}


print "Total images:   " . count($widths) . PHP_EOL;

print "Average width:  " . round(array_sum($widths)/count($widths)) . "px";
print " [" . min($widths) . "px - " . max($widths) . "px] @ " . round(stats_standard_deviation($widths)) . "px" . PHP_EOL;
print "Average height: " . round(array_sum($heights)/count($heights)) . "px";
print " [" . min($heights) . "px - " . max($heights) . "px] @ " . round(stats_standard_deviation($heights)) . "px" . PHP_EOL;

exit(0);
