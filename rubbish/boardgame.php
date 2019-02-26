<?php

$csv = array_map('str_getcsv', file('./content-event-events - content-event-events.csv'));

// Remove table header
array_shift($csv);

$all = array();

function cmp($l, $r) {
	return $r["score"] - $l["score"];
}

$games_with_bacteria = 0;
$games_with_virus = 0;
$games_total = 0;

$win_bacteria = 0;
$win_virus = 0;

$mut = 0;
$mut_win_bacteria = 0;
$mut_win_virus = 0;

$win_scores_bacteria = [];
$win_scores_virus = [];

foreach($csv as $row) {
	
	$label = $row[0];
	$count = $row[1];
		
	// Skip AI
	if(strpos($label, "Opponent") !== false) {
		continue;
	}
	
	$players = explode(" ", $label);
	
	$scores = array(
		"count" => $count,
		"players" => array(),
		"row" => $row[0]
	);
	
	
	
	$hasvirus = false;
	$hasbacteria = false;
	
	foreach($players as $player) {
		
		if(strpos($player, "-") !== false) {
			list($type, $score) = explode("-", $player);
			
			if($type == "Virus") {
				$hasvirus = true;
			} else if($type == "Bacteria") {
				$hasbacteria = true;
			} else {
				assert(false, "unknown type " . $type);
			}
			
			array_push($scores["players"], array("score" => $score, "type" => $type));
		}
	}
	
	
	usort($scores["players"], cmp);
	
	if($hasbacteria && $hasvirus) {
		$mut += $count;
	}
	
	if(count($scores["players"]) > 0) {
		$games_with_bacteria += $hasbacteria * $count;
		$games_with_virus += $hasvirus * $count;
		$games_total += $count;
	
		array_push($all, $scores);
		
		$winner = $scores["players"][0];
		
		if($winner["type"] == "Virus") {
			$win_virus += $count;
			
			if($hasbacteria) {
				$mut_win_virus += $count;
			}
			
		} else {
			$win_bacteria += $count;
			
			if($hasvirus) {
				$mut_win_bacteria += $count;
			}
		}
		
		// Gather all winner scores
		for($i = 0; $i < $count; ++$i) {
			if($winner["type"] == "Virus") {
				array_push($win_scores_virus, $winner["score"]);
			} else {
				array_push($win_scores_bacteria, $winner["score"]);
			}
		}
		
	}
}

printf("There are %d games recorded\n", $games_total);
printf(" of which %.0f%% has a bacteria\n", $games_with_bacteria / $games_total * 100);
printf(" of which %.0f%% has a virus\n", $games_with_virus / $games_total * 100);
printf(" of which bacteria won %.0f%% games\n", $win_bacteria / $games_total * 100);
printf(" of which virus won %.0f%% games\n", $win_virus / $games_total * 100);
printf("\n");

printf("If a game has a bacteria, it won %.4f%% of those games\n", $mut_win_bacteria / $mut * 100);
printf("If a game has a virus, it won %.4f%% of those games\n", $mut_win_virus / $mut * 100);

printf("\n");
printf("bacteria mean winning score is %d pts\n", array_sum($win_scores_bacteria) / count($win_scores_bacteria));
printf("virus mean winning score is %d pts", array_sum($win_scores_virus) / count($win_scores_virus));


foreach(array("virus" => $win_scores_virus,  "bacteria" => $win_scores_bacteria) as $type => $scores) {

	$lookup = [];
	
	foreach($scores as $score) {
		if( ! isset($lookup[$score])) {
			$lookup[$score] = 0;
		}
		
		++$lookup[$score];
	}
	
	// Sort by score
	ksort($lookup);
	
	$csv = "";
	
	for($i = 0; $i < 300; ++$i) {
		
		$count = 0;
		if(isset($lookup[$i])) {
			$count = $lookup[$i];
		}
		
		$csv .= $i . "," . $count . "\n";
	}	
	
	file_put_contents($type . ".csv", $csv);
	
	/*
	foreach($lookup as $score => $count) {
		print($score . "," . $count . "\n");
	}
	*/
}

// Of games with virus, virus is X chance to win
