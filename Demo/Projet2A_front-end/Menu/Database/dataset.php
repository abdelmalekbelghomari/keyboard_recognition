<?php
$variable = isset($_GET['variable']) ? $_GET['variable'] : '';

if (!empty($variable)) {
    $audioDirectory = "Audio";
    $textFile = "Audio/text.txt";
    $lines = file($textFile, FILE_IGNORE_NEW_LINES);
} else {
    die("No variable");
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Page avec Texte et Audio</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            font-family: 'Arial', sans-serif;
            background-color: #f2f2f2; 
            color: #333; 
        }

        .content {
            text-align: center;
            padding: 20px;
            margin: 50px auto;
            max-width: 600px;
            background-color: #fff; 
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); 
        }

        h1 {
            font-size: 2em;
            margin: 10px 0;
            white-space: nowrap;
            overflow: hidden;
            border-right: 3px solid #333;
            animation: typing 2s steps(30);
        }

        p {
            margin: 10px 0;
            font-size: 1.2em;
        }

        audio {
            margin-top: 20px;
            width: 100%;
        }

        @keyframes typing {
            from {
                width: 0;
            }
            to {
                width: 100%;
            }
        }

    </style>
</head>
<body>
    <div class="content">
        <h1 id="menu-title"><?php echo ucfirst($variable) . "'s Dataset" ?></h1>

        <?php
            foreach ($lines as $index => $line) {
                $audioFile = $audioDirectory . "/" . $variable . "/" . $variable . ($index + 1) . ".wav";
                echo "<p>".$line."</p>";
                echo "<audio controls>
                <source src=".$audioFile." type='audio/wav'>
                Le navigateur ne prend pas en charge l'élément audio.
                </audio>";
            }
        ?>
    </div>
</body>
</html>
