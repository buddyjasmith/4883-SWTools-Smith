<?php
//Buddy Smith
//February 28,2019
//Description: This program processes stats based upon nfl data


//Connect to mysql
$host = "localhost";             // because we are ON the server
$user = "********";        // user name

// Get username and password from slack
// The DB username and pass not the ones
// I sent you to log into the server.
$password = "**************";         // password 
$database = "******";              // database 
$mysqli = mysqli_connect($host, $user, $password, $database);

if (mysqli_connect_errno($mysqli)) {
    echo "Failed to connect to MySQL: " . mysqli_connect_error();
}


/**
 * This function runs a SQL query and returns the data in an associative array
 * that looks like:
 * $response [
 *      "success" => true or false
 *      "error" => contains error if success == false
 *      "result" => associative array of the result
 * ]
 *
 */
function getPlayer($playerId){
    global $mysqli;
    $sql = "SELECT `name` FROM players WHERE id = '{$playerId}' LIMIT 1";
    $response = runQuery($mysqli,$sql); 
    if(!array_key_exists('error',$response)){
        return $response['result'][0]['name'];
    }
    return null;
}
function runQuery($mysqli,$sql){
    $response = [];

    // run the query
    $result = $mysqli->query($sql);

    // If we were successful
    if($result){
        $response['success'] = true;
        // loop through the result printing each row
        while($row = $result->fetch_assoc()){
            $response['result'][] = $row;
        }
        $result->free();
    }else{
        $response['success'] = false;
        $response['error'] = $mysqli->error;
    }

    return $response;
}






//count penalties divided by number of seasons

//rank nfl by win loss percentage



echo "<pre>";   // so whitespace matters

//Question 1
$sql = "SELECT id, name, COUNT(DISTINCT club) as teamCnt 
         FROM `players`
         GROUP by id ORDER by teamCnt DESC Limit 10";
$count = 0;
echo("Question 1: Count number of teams an individual player played for.\n");
echo("==================================================================\n");
echo str_pad("#\tPlayerID",20);
echo str_pad("Name",20);
echo str_pad("#Teams",20);
echo("\n");
$response =runQuery($mysqli,$sql);
if($response['success']){
    foreach($response['result'] as $row){
        echo str_pad("$count",8);
        echo str_pad("{$row['id']}",18);
        echo str_pad("{$row['name']}",20);
        echo("{$row['teamCnt']}\n");
        
        $count = $count +1;
    }
}
//Question 2
/******************************************************************************************************************************************** */
$sql = "SELECT playerid, season, sum(yards) as yards 
         FROM `players_stats` 
         WHERE statid=10 or statid=75 or statid=76 
         GROUP BY season, playerid 
         ORDER BY yards 
         DESC LIMIT 5";
echo("\n\n\nQuestion 2: Find the players with the highest total rushing yards by year, and limit the result to top 5\n\n");
echo("============================================================================================\n");
echo str_pad("#\t",8);
echo str_pad("PlayerID",20);
echo str_pad("Name",20);
echo str_pad("Year",20);
echo("# Yards\n");
$count = 0;
$response = runQuery($mysqli,$sql);
 if($response['success']){
     foreach($response['result'] as $row){
         echo str_pad("$count",14);
         $row['player'] = getPlayer($row['playerid']);
         echo str_pad("{$row['playerid']}",20);
         echo str_pad("{$row['player']}",20);
         echo str_pad("{$row['season']}",20);
         echo ("{$row['yards']}\n");
        
       
        
        $count = $count +1;
     }
 }
 else{
     echo("Error");
}
//Question 3
/********************************************************************************************************************************************* */
$sql = "SELECT playerid, season, sum(yards) as yards 
        FROM players_stats 
        WHERE statid=15 
        GROUP BY season, playerid
        ORDER BY yards 
        ASC LIMIT 5";
echo("\n\n\nQuestion 3: Find the bottom 5 passing players per year\n\n");
echo("============================================================================================\n");
echo str_pad("#\t",8);
echo str_pad("PlayerID",20);
echo str_pad("Name",20);
echo str_pad("Year",20);
echo("# Yards\n");
$count = 0;
$response = runQuery($mysqli,$sql);
if($response['success']){
    foreach($response['result'] as $row){
        echo str_pad("$count",14);
        $row['player'] = getPlayer($row['playerid']);
        echo str_pad("{$row['playerid']}",20);
        echo str_pad("{$row['player']}",20);
        echo str_pad("{$row['season']}",20);
        echo ("{$row['yards']}\n");
       
      
       
       $count = $count +1;
    }
}
else{
    echo("Error");
}

//Question 4
/************************************************************************ */
$sql = "SELECT playerid, season,sum(yards) as total
from players_stats 
where statid ='10'  and yards < 0
group by season, playerid 
order by total asc
LIMIT 5";
echo("\n\n\nQuestion 4: Find the top 5 players that had the most rushes for a loss.\n\n");
echo("============================================================================================\n");
echo str_pad("#\t",8);
echo str_pad("PlayerID",20);
echo str_pad("Name",20);
echo str_pad("Year",20);
echo("# Yards\n");
$count = 0;
$response = runQuery($mysqli,$sql);
if($response['success']){
    foreach($response['result'] as $row){
        echo str_pad("$count",14);
        $row['player'] = getPlayer($row['playerid']);
        echo str_pad("{$row['playerid']}",20);
        echo str_pad("{$row['player']}",20);
        echo str_pad("{$row['season']}",20);
        echo ("{$row['total']}\n");
       
      
       
       $count = $count +1;
    }
}
else{
    echo("Error");
}


//Question 5
/************************************************************************* */
$sql ="SELECT club, sum(pen) as penalties
        FROM `game_totals`
        GROUP BY club
        ORDER BY penalties DESC 
        LIMIT 5";

echo("\n\n\nQuestion 5: Find the top 5 teams with the most penalties.\n\n");
echo("============================================================================================\n");
echo str_pad("#\t",8);
echo str_pad("Club",20);
echo("# Penalties\n");

$count = 1;
$response = runQuery($mysqli,$sql);
if($response['success']){
    foreach($response['result'] as $row){
        echo str_pad("$count",14);
        echo str_pad("{$row['club']}",20);
        echo ("{$row['penalties']}\n");
        
       
      
       
       $count = $count +1;
    }
}
else{
    echo("Error");
}

//Question 6
/************************************************************************** */
$sql = "SELECT season, sum(pen) as 'Total Penalties',  sum(pen) / count(gameid) as penalties
FROM `game_totals`
GROUP BY season
order by season asc";

echo("\n\n\nQuestion 6: Find the average number of penalties per season.\n\n");
echo("============================================================================================\n");
echo str_pad("#\t",8);
echo str_pad("Season",20);
echo str_pad("Total Penalties",20);
echo("Average Penalties\n");

$count = 1;
$response = runQuery($mysqli,$sql);
if($response['success']){
    foreach($response['result'] as $row){
        echo str_pad("$count",14);
        echo str_pad("{$row['season']}",20);
        echo str_pad("{$row['Total Penalties']}",20);
        echo ("{$row['penalties']}\n");
        
       
      
       
       $count = $count +1;
    }
}
else{
    echo("Error");
}

//Question 7
/**************************************************************************** */
$sql = "SELECT club,season,count(DISTINCT playid)/16 as average
FROM `players_stats`
group by season, club
order by average asc
LIMIT 10";
echo("\n\n\nQuestion 7: Find the Team with the least amount of average plays every year.\n\n");
echo("============================================================================================\n");
echo str_pad("#\t",8);
echo str_pad("Club",20);
echo str_pad("Season",20);
echo("Average Plays\n");

$count = 1;
$response = runQuery($mysqli,$sql);
if($response['success']){
    foreach($response['result'] as $row){
        echo str_pad("$count",14);
        echo str_pad("{$row['club']}",20);
        echo str_pad("{$row['season']}",20);
        echo ("{$row['average']}\n");     
        $count = $count +1;
    }
}
else{
    echo("Error");
}

//Question 8
/********************************************************************* */
$sql = "SELECT playerid, count(statid) as total
FROM `players_stats`
where statid = 70 and yards > 40
group by playerid
order by total desc
LIMIT 5";
echo("\n\n\nQuestion 8: Find the top 5 players that had field goals over 40 yards.\n\n");
echo("============================================================================================\n");
echo str_pad("#\t",8);
echo str_pad("Name",20);
echo str_pad("PlayerID",20);
echo("FG > 40 yards\n");

$count = 1;
$response = runQuery($mysqli,$sql);
if($response['success']){
    foreach($response['result'] as $row){
        echo str_pad("$count",14);
        $row['player'] = getPlayer($row['playerid']);
        echo str_pad("{$row['player']}",20); 
        echo str_pad("{$row['playerid']}",20);  
        echo("{$row['total']}\n") ; 
        $count = $count +1;
    }
}
else{
    echo("Error");
}


//Question 9
/************************************************************************* */
$sql = "SELECT playerid, count(statid) as total, sum(yards)/count(statid) as average
FROM `players_stats`
where statid = 70 
group by playerid
order by total asc
limit 5";
echo("\n\n\nQuestion 9: Find the top 5 players with the shortest avg field goal length.\n\n");
echo("============================================================================================\n");
echo str_pad("#\t",8);
echo str_pad("Name",20);
echo str_pad("PlayerID",20);
echo("Average Length\n");

$count = 1;
$response = runQuery($mysqli,$sql);
if($response['success']){
    foreach($response['result'] as $row){
        echo str_pad("$count",14);
        $row['player'] = getPlayer($row['playerid']);
        echo str_pad("{$row['player']}",20); 
        echo str_pad("{$row['playerid']}",20);  
        echo("{$row['average']}\n") ; 
        $count = $count +1;
    }
}
else{
    echo("Error");
}
echo("Question 10: Rank the NFL by win loss percentage (worst first).\n");
echo("Haven't finished this yet.\n");

echo("Question 11:Find the top 5 most common last names in the NFL.\n");
echo("Haven't finished this yet.\n");

