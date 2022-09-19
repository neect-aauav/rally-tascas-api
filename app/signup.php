<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="css/styles.css">
    <link rel="stylesheet" href="css/signup.css">
    <title>Signup | Rallyween</title>
</head>
<body>
    <div class="signup-form absolute-centered">
        <p>Equipa</p>
        <form action="signup.php" method="post">
            <div class="team">
                <input placeholder="Nome" type="text" name="team">
                <input placeholder="Email" type="email" name="email">           
            </div>
            <div class="members">
                <div>Membros</div>
                <div>
                    <input placeholder="Nome" type="text" name="member">
                    <select name="course">
                        <option></option>
                    </select>
                </div>
                <div class="add-member clickable">+ Adicionar Membro</div>
            </div>
            <button class="clickable" type="submit">Criar</button>
        </form>
    </div>
    
    <script src="scripts/static.js"></script>
    <script src="scripts/signup.js"></script>
</body>
</html>