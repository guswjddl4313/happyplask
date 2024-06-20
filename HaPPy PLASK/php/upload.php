<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (isset($_FILES['file']) && $_FILES['file']['error'] === UPLOAD_ERR_OK) {
        $upload_dir = 'uploads/';
        $uploaded_file = $upload_dir . basename($_FILES['file']['name']);

        // Ensure the upload directory exists
        if (!is_dir($upload_dir)) {
            mkdir($upload_dir, 0755, true);
        }

        // Move the uploaded file to the specified directory
        if (move_uploaded_file($_FILES['file']['tmp_name'], $uploaded_file)) {
            echo 'File uploaded successfully';
        } else {
            echo 'Failed to move uploaded file';
        }
    } else {
        echo 'No file uploaded or file upload error';
    }
} else {
    echo 'Invalid request method';
}
?>

