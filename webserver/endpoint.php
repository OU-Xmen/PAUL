<?php
// [ Debug ]
// ini_set('display_errors', '1');
// ini_set('display_startup_errors', '1');
// error_reporting(E_ALL);

// Check if the request is a POST request
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Check if name and score POST variables are set
    if (isset($_POST['name']) && isset($_POST['score']) && isset($_POST['game'])) {
        // Proceed to insert data into database
        $task = "insert_score";
        // Get name from POST variable
        $name = $_POST['name'];
        // Get score from POST variable
        $score = $_POST['score'];
        // Get game from POST variable
        $game = $_POST['game'];
        // Convert score to integer
        $score = intval($score);
        // Remove everything except letters, numbers, spaces, and underscores from name
        $name = preg_replace("/[^a-zA-Z0-9_ ]+/", "", $name);
        // Remove everything except letters, numbers, spaces, and underscores from game
        $game = preg_replace("/[^a-zA-Z0-9_ ]+/", "", $game);
    }
    else {
        // Just return the top 10 scores
        $task = "get_scores";
    }
}
else {
    // Just return the top 10 scores
    $task = "get_scores";
}

// [ Debug ]
// $task = "insert_score";
// $name = "Paul";
// $game = "test";
// $score = 100;

// Get database info from json file in db_config.json in config folder
$db_config = json_decode(file_get_contents('config/db_config.json'), true);

// Connect to database
$host = $db_config['host'];
$user = $db_config['user'];
$pass = $db_config['pass'];
$db = $db_config['db'];
$port = $db_config['port'];

// Create connection
$conn = mysqli_connect ($host, $user, $pass, $db, $port);

// If connected, insert data
if ($conn) {
    // Preemptively set success to false
    $success = false;

    // If task is to insert score
    if ($task == "insert_score") {
        $date = date("Y-m-d H:i:s");
        // Insert score into database
        $sql = "INSERT INTO highscores (name, score, game, date) VALUES (?, ?, ?, ?)";
        $stmt = $conn->prepare($sql);
        $stmt->bind_param("siss", $name, $score, $game, $date);
        $stmt->execute() or trigger_error($stmt->error);
        $conn->close();
        // Return success message
        echo "Paul says: Score inserted successfully";
        $success = true;
    }

    // If task is to get scores
    if ($task == "get_scores") {
        // Make a function to return the json string for each game
        function get_game_scores($game) {
            global $conn;
            $sql = "SELECT name, score FROM highscores WHERE game = ? ORDER BY score DESC LIMIT 10";
            $stmt = $conn->prepare($sql);
            $stmt->bind_param("s", $game);
            $stmt->execute() or trigger_error($stmt->error);
            $result = $stmt->get_result();
            // Create string of top 10 scores for game
            $game_string = "";
            while ($row = $result->fetch_assoc()) {
                $game_string .= $row['name'] . ":::" . $row['score'] . ",";
            }
            // Remove last comma
            $game_string = rtrim($game_string, ",");
            return $game_string;
        }

        // Define the list of games
        $games = array('Puzzle', 'Asteroids', 'Tetris', 'Pong', 'Hangman', 'Mad Libs', 'Checkers', 'Chess', 'Guess the Number', 'Snake', 'Tic Tac Toe', 'Connect 4', 'Mancala', 'RPS', 'PAULatformer');

        // Get top 10 scores for each game, saving each in the name of the game
        $game_full_string = array();
        // For every game in the list of games, get the top 10 scores
        foreach ($games as $game) {
            $game_full_string[$game] = get_game_scores($game);
        }

        // Return and print top 10 scores for each game
        echo json_encode($game_full_string);
        $success = true;
        $conn->close();
    }
}
else {
    die ("Connection failed: " . mysqli_connect_error());
}
?>
