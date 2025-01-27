<?php
// Ścieżka do pliku JSON
$file_path = './pythonProject1/teams_data.json';

// Sprawdzenie, czy plik istnieje
if (file_exists($file_path)) {
    // Odczyt danych z pliku
    $data = file_get_contents($file_path);

    // Dekodowanie danych JSON
    $teams = json_decode($data, true);
} else {
    echo "Plik JSON nie istnieje.";
}

?>

<!DOCTYPE html>
<html lang="pl">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <link rel="stylesheet" href="./style1.css">
</head>

<body>
    <?php
    echo "<div class='wrapper'>";
    if ($teams) {
        // Iteracja po drużynach i wyświetlanie danych
        echo "<form action='./getdata.php' method='GET'>";
        foreach ($teams as $team) {
            echo "
                
                <button type='submit' name='teamname' value='" . $team['team_name'] . "'>
                " . $team['team_name'] . "
                </button><br>
            ";
        }
        echo "</form>";
    } else {
        echo "Błąd: Nie udało się zdekodować danych JSON.";
    }
    echo "</div>";
    ?>
</body>

</html>