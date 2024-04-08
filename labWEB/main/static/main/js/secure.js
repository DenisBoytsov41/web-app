const jwtToken = "<?php echo isset($_GET['token']) && isset($_SESSION['jwt']) && $_SESSION['jwt'] !== '' ? $_SESSION['jwt'] : ''; ?>";
if (jwtToken) {
    fetch('protected_resource.php', {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${jwtToken}`
        }
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Ошибка HTTP: ' + response.status);
            }
            return response.json();
        })
        .then(data => {
            console.log(data);
            const dataContainer = document.getElementById('dataContainer');
            if (dataContainer) {
                dataContainer.textContent = JSON.stringify(data);
            }
        })
        .catch(error => {
            console.error('Ошибка:', error);
        });
} else {
    console.log('Токен отсутствует');
    const dataContainer = document.getElementById('dataContainer');
    if (dataContainer) {
        dataContainer.textContent = 'Доступ запрещен для гостей';
    }
}
