fetch('/metadata.json')
    .then(r => r.json())
    .then(data => {
        const grid = document.getElementById('metadata-grid');
        const items = [
            { icon: '🏷️', label: 'Instance ID', value: data.instance_id },
            { icon: '⚙️', label: 'Type', value: data.instance_type },
            { icon: '📍', label: 'Zone', value: data.az },
            { icon: '🌍', label: 'Région', value: data.region },
            { icon: '🌐', label: 'IP Public', value: data.public_ip },
            { icon: '🔒', label: 'IP Privée', value: data.private_ip },
            { icon: '💾', label: 'AMI', value: data.ami_id.substring(0, 12) + '...' },
            { icon: '⏰', label: 'Créée', value: data.created_date },
        ];

        grid.innerHTML = items.map(item => `
            <div class="bg-gray-800/50 backdrop-blur border border-gray-700 rounded-lg p-4 hover:border-blue-500/50 transition">
                <p class="text-gray-400 text-sm">${item.icon} ${item.label}</p>
                <p class="font-mono text-sm text-blue-300 break-all">${item.value}</p>
            </div>
        `).join('');

        document.getElementById('update-time').textContent = `Mis à jour le ${data.created_date}`;
    })
    .catch(err => {
        console.error('Erreur:', err);
        document.getElementById('metadata-grid').innerHTML = 
            '<div class="col-span-4 text-red-400">Erreur de chargement des données</div>';
    });
