<?php
// Formulaire du site Cabinet Valorys : enregistre chaque demande, puis l'envoie par email.
// 1) Chaque demande est TOUJOURS enregistrée dans un journal (aucune demande perdue).
// 2) Envoi par SMTP authentifié si le fichier valorys-smtp.php existe, sinon par mail() d'OVH.
header('Content-Type: application/json; charset=utf-8');
date_default_timezone_set('Europe/Paris');
$DEST = 'contact@cabinet-valorys.com';   // boîte qui reçoit les demandes (CONTACT VALORYS)
$FROM = 'contact@cabinet-valorys.com';

function out($ok, $err = '') { echo json_encode(['ok' => $ok, 'error' => $err], JSON_UNESCAPED_UNICODE); exit; }
if ($_SERVER['REQUEST_METHOD'] !== 'POST') { http_response_code(405); out(false, 'Méthode non autorisée.'); }

$in = json_decode(file_get_contents('php://input'), true);
if (!is_array($in)) $in = $_POST;

// Anti-spam : champ piège rempli, ou envoi en moins de 3 secondes
if (!empty($in['website'])) out(true);
if (isset($in['elapsed']) && (int)$in['elapsed'] < 3000) out(true);

$line = function ($k, $max) use ($in) {
  $v = isset($in[$k]) ? trim((string)$in[$k]) : '';
  return mb_substr(strip_tags(str_replace(["\r", "\n"], ' ', $v)), 0, $max);
};
$name = $line('name', 100); $email = $line('email', 150); $phone = $line('phone', 30); $type = $line('request_type', 120);
$message = isset($in['message']) ? mb_substr(strip_tags(trim((string)$in['message'])), 0, 2000) : '';
$callback = !empty($in['callback']);
$slot = $line('slot', 60);

if (mb_strlen($name) < 2) out(false, $callback ? "Merci d'indiquer votre prénom." : 'Merci de renseigner votre nom.');
if ($callback) {
  if (strlen(preg_replace('/\D/', '', $phone)) < 9) out(false, 'Merci de vérifier votre numéro de téléphone.');
} elseif (!filter_var($email, FILTER_VALIDATE_EMAIL)) out(false, 'Merci de vérifier votre adresse email.');
if (empty($in['consent'])) out(false, 'Merci de cocher la case de consentement pour que nous puissions vous recontacter.');

$when = date('d/m/Y H:i');
if ($callback) {
  $subject = 'À RAPPELER : ' . $name . ' — ' . $phone . ($slot ? " ($slot)" : '');
  $body = "Demande de rappel\n\nNom : $name\nTéléphone : $phone\nCréneau : $slot\nSujet : $type\n\n---\nEnvoyé le $when depuis cabinet-valorys.com (consentement donné).";
} else {
  $subject = 'Demande site : ' . ($type ?: 'contact') . ' — ' . $name;
  $body = "Nom : $name\nEmail : $email\nTéléphone : $phone\nType de demande : $type\n\nMessage :\n$message\n\n---\nEnvoyé le $when depuis cabinet-valorys.com (consentement donné).";
}

// ---------- Email HTML aux couleurs du cabinet ----------
function h($v) { return htmlspecialchars((string)$v, ENT_QUOTES, 'UTF-8'); }
function email_html($callback, $name, $email, $phone, $slot, $type, $message, $when) {
  $navy = '#1B2A4A'; $red = '#C0392B'; $muted = '#5b6475'; $line = '#E6E8EE';
  $telLink = 'tel:' . preg_replace('/[^0-9+]/', '', $phone);
  $badge = $callback ? 'Demande de rappel' : 'Nouveau message';
  $title = $callback ? 'Un visiteur souhaite être rappelé' : 'Un visiteur vous a écrit';
  $row = function ($label, $value, $strong = false) use ($muted, $line, $navy) {
    if ($value === '' || $value === null) return '';
    $v = $strong ? '<strong style="color:' . $navy . ';font-size:17px;">' . $value . '</strong>' : $value;
    return '<tr><td style="padding:12px 0;border-bottom:1px solid ' . $line . ';color:' . $muted . ';font-size:13px;text-transform:uppercase;letter-spacing:.06em;width:38%;vertical-align:top;">' . $label . '</td>'
         . '<td style="padding:12px 0;border-bottom:1px solid ' . $line . ';color:#1b1b1e;font-size:15px;vertical-align:top;">' . $v . '</td></tr>';
  };
  $rows  = $row('Nom', h($name), true);
  $rows .= $row('Téléphone', $phone ? '<a href="' . h($telLink) . '" style="color:' . $navy . ';text-decoration:none;font-weight:bold;">' . h($phone) . '</a>' : '');
  $rows .= $row('Email', $email ? '<a href="mailto:' . h($email) . '" style="color:' . $navy . ';">' . h($email) . '</a>' : '');
  if ($callback) $rows .= $row('Créneau souhaité', '<span style="display:inline-block;background:#FDEDEB;color:' . $red . ';font-weight:bold;padding:4px 12px;border-radius:20px;">' . h($slot) . '</span>');
  $rows .= $row('Sujet', h($type));
  $msg = $message !== '' ? '<tr><td colspan="2" style="padding:18px 0 4px;"><div style="color:' . $muted . ';font-size:13px;text-transform:uppercase;letter-spacing:.06em;margin-bottom:8px;">Message</div>'
       . '<div style="background:#F5F3F6;border-left:4px solid ' . $red . ';padding:14px 16px;color:#1b1b1e;font-size:15px;line-height:1.6;">' . nl2br(h($message)) . '</div></td></tr>' : '';
  $btns = '';
  if ($phone) $btns .= '<a href="' . h($telLink) . '" style="display:inline-block;background:' . $red . ';color:#ffffff;text-decoration:none;font-weight:bold;font-size:15px;padding:14px 26px;border-radius:40px;margin:0 8px 10px 0;">Appeler ' . h($phone) . '</a>';
  if ($email) $btns .= '<a href="mailto:' . h($email) . '" style="display:inline-block;background:' . $navy . ';color:#ffffff;text-decoration:none;font-weight:bold;font-size:15px;padding:14px 26px;border-radius:40px;margin:0 8px 10px 0;">Répondre par email</a>';
  return '<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>'
  . '<body style="margin:0;padding:0;background:#EEF0F4;font-family:Arial,Helvetica,sans-serif;">'
  . '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#EEF0F4;"><tr><td align="center" style="padding:28px 12px;">'
  . '<table role="presentation" width="600" cellpadding="0" cellspacing="0" style="width:100%;max-width:600px;background:#ffffff;border-radius:10px;overflow:hidden;">'
  . '<tr><td style="background:' . $navy . ';padding:26px 32px;border-bottom:4px solid ' . $red . ';"><img src="cid:logo" width="170" alt="Cabinet Valorys" style="display:block;border:0;width:170px;height:auto;"></td></tr>'
  . '<tr><td style="padding:30px 32px 6px;">'
  . '<span style="display:inline-block;background:' . $red . ';color:#ffffff;font-size:12px;font-weight:bold;text-transform:uppercase;letter-spacing:.08em;padding:5px 12px;border-radius:20px;">' . $badge . '</span>'
  . '<h1 style="margin:16px 0 6px;color:' . $navy . ';font-size:24px;line-height:1.25;">' . $title . '</h1>'
  . '<p style="margin:0;color:' . $muted . ';font-size:14px;">Reçu le ' . h($when) . ' depuis le site cabinet-valorys.com</p>'
  . '</td></tr>'
  . '<tr><td style="padding:16px 32px 8px;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0">' . $rows . $msg . '</table></td></tr>'
  . '<tr><td style="padding:20px 32px 26px;">' . $btns . '</td></tr>'
  . '<tr><td style="background:#F5F3F6;padding:16px 32px;color:' . $muted . ';font-size:12px;line-height:1.6;">Le visiteur a accepté d\'être recontacté au sujet de sa demande. Cette demande est aussi enregistrée dans le journal du site.</td></tr>'
  . '</table></td></tr></table></body></html>';
}

// ---------- 1. Journal des demandes (hors du dossier public si possible) ----------
function journal_dir() {
  $out = dirname(__DIR__) . '/demandes-site';           // ex. /home/cabingw/demandes-site
  if (is_dir($out) || @mkdir($out, 0750, true)) { if (is_writable($out)) return $out; }
  $in = __DIR__ . '/_demandes';                          // repli : dossier protégé dans le site
  if (!is_dir($in)) { @mkdir($in, 0750, true); @file_put_contents("$in/.htaccess", "Require all denied\nDeny from all\n"); }
  return $in;
}
function journal($row) {
  $f = journal_dir() . '/demandes.csv';
  $new = !file_exists($f);
  if ($h = @fopen($f, 'a')) {
    if ($new) { fwrite($h, "\xEF\xBB\xBF"); fputcsv($h, ['Date', 'Type', 'Nom', 'Email', 'Téléphone', 'Créneau', 'Sujet', 'Message', 'Envoi email'], ';'); }
    fputcsv($h, $row, ';'); fclose($h); return true;
  }
  return false;
}

// ---------- 2. Envoi de l'email ----------
$sent = false; $how = ''; $err = '';
$cfgFile = dirname(__DIR__) . '/valorys-smtp.php';     // fichier privé, hors du site (voir LISEZ-MOI)
if (file_exists($cfgFile)) {
  $cfg = include $cfgFile;
  require __DIR__ . '/lib/phpmailer/Exception.php';
  require __DIR__ . '/lib/phpmailer/PHPMailer.php';
  require __DIR__ . '/lib/phpmailer/SMTP.php';
  $m = new PHPMailer\PHPMailer\PHPMailer(true);
  try {
    $m->isSMTP(); $m->CharSet = 'UTF-8';
    $m->Host = $cfg['host']; $m->Port = (int)$cfg['port']; $m->SMTPAuth = true;
    $m->Username = $cfg['user']; $m->Password = $cfg['pass'];
    $m->SMTPSecure = ((int)$cfg['port'] === 465) ? 'ssl' : 'tls';
    $m->setFrom($cfg['user'], 'Site Cabinet Valorys');
    $m->addAddress($DEST);
    if ($email) $m->addReplyTo($email, $name);
    $m->Subject = $subject;
    $m->isHTML(true);
    $m->Body = email_html($callback, $name, $email, $phone, $slot, $type, $message, $when);
    $m->AltBody = $body;
    $logo = __DIR__ . '/lib/logo-mail.png';
    if (file_exists($logo)) $m->addEmbeddedImage($logo, 'logo', 'valorys.png');
    $m->send(); $sent = true; $how = 'SMTP';
  } catch (Throwable $e) { $err = 'SMTP : ' . $m->ErrorInfo; }
}
if (!$sent) {
  $headers = "From: Site Cabinet Valorys <$FROM>\r\n" . ($email ? "Reply-To: $email\r\n" : '') . "MIME-Version: 1.0\r\nContent-Type: text/plain; charset=UTF-8\r\nContent-Transfer-Encoding: 8bit";
  $sent = @mail($DEST, '=?UTF-8?B?' . base64_encode($subject) . '?=', $body, $headers, '-f' . $FROM);
  $how = $sent ? 'mail() OVH' : ($err ? $err . ' / mail() refusé' : 'mail() refusé');
}

$saved = journal([$when, $callback ? 'Rappel' : 'Message', $name, $email, $phone, $slot, $type, str_replace(["\r", "\n"], ' ', $message), $how]);

// Le visiteur voit un succès dès que sa demande est conservée (email ou journal).
if ($sent || $saved) out(true);
out(false, "L'envoi a échoué. Écrivez-nous à $DEST ou appelez le 06 69 94 56 08.");
