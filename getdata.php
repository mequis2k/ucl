<?php
// decode
$json_data = file_get_contents('./pythonProject1/teams_data.json');
$teams = json_decode($json_data, true);

// get team from main page
$selected = $_GET['teamname'];
$position = null;

// dobieranie pozycji do wybranej drużyny.
foreach ($teams as $team) {
    if ($team['team_name'] == $selected) {
        $position = $team['position'];
        break;
    }
}



?>
<!DOCTYPE html>
<html lang="pl">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?php echo $selected; ?> - Opponents in the next round</title>
    <link rel="stylesheet" href="./style.css">
</head>

<body>
    <div class="wrapper">

        <?php
        // sprawdzanie kolejnej fazy drużyny
        if ($position >= 1 && $position <= 8) {
            echo "<h1 class='informacja'>Next phase: Round of 16.</h1><br><h2 class='informacja-h2'>Next round's possible teams:</h2>";
        } elseif ($position >= 9 && $position <= 24) {
            echo "<h1 class='informacja'>Next phase: Knockout phase play-offs.</h1><br><h2 class='informacja-h2'>Next round's possible teams:</h2>";
        } else {
            echo "<h1 class='informacja'>Your team does not qualify for the next phase at this moment.</h1>";
        }
        if ($position <= 24) {
            switch ($position) {
                case 1:
                case 2:
                    $next = ['15', '16', '17', '18'];
                    break;
                case 3:
                case 4:
                    $next = ['13', '14', '19', '20'];
                    break;
                case 5:
                case 6:
                    $next = ['11', '12', '21', '22'];
                    break;
                case 7:
                case 8:
                    $next = ['9', '10', '23', '24'];
                    break;
                case 9:
                case 10:
                    $next = ['23', '24'];
                    break;
                case 11:
                case 12:
                    $next = ['21', '22'];
                    break;
                case 13:
                case 14:
                    $next = ['19', '20'];
                    break;
                case 15;
                case 16:
                    $next = ['17', '18'];
                    break;
                case 17;
                case 18:
                    $next = ['15', '16'];
                    break;
                case 19;
                case 20:
                    $next = ['13', '14'];
                    break;
                case 21;
                case 22:
                    $next = ['11', '12'];
                    break;
                case 23;
                case 24:
                    $next = ['9', '10'];
                    break;
            };
            echo "<div class='team_name_wrapper'>";
            foreach ($teams as $team) {
                if (in_array($team['position'], $next)) {
                    echo "<p class='team_name'>" . $team['team_name'] . "</p> <br>";
                }
            };
            echo "</div>";
        }

        ?>
    </div>

</body>

</html>