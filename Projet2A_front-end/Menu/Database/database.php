<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="../menu.css">
    <script src="https://code.jquery.com/jquery-3.6.4.min.js"></script>
    <title>Menu</title>
</head>
<body>
    <div class="hacker-background">
        <div class="content">
            <h1 id="menu-title">Menu/Database</h1>
            <ul class="menu-list">
                <li><a href="#" id="cedric-link">Cedric's Dataset</a></li>
                <li><a href="#" id="fabrice-link">Fabrice's Dataset</a></li>
                <li><a href="../menu.php">..</a></li>
            </ul>
        </div>
    </div>
    <script>
        $(document).ready(function() {
            $("#cedric-link").click(function() {
                navigateToNextPage("cedric");
            });

            $("#fabrice-link").click(function() {
                navigateToNextPage("fabrice");
            });

            function navigateToNextPage(variableValue) {
                window.location.href = "dataset.php?variable=" + encodeURIComponent(variableValue);
            }
        });
    </script>
</body>
</html>
