const discord = require('discord.js');
const client = new discord.Client();
const avis_channel_id = '1081294505019461742'; // L'ID du salon d'avis

client.on('ready', async () => {
  console.log(`Logged in as ${client.user.tag}!`);

  const avis_channel = client.channels.cache.get(avis_channel_id);
  const messages = await avis_channel.messages.fetch();

  const total_notes = messages.reduce((total, message) => {
    const note = parseInt(message.embeds[0].fields[0].value.split('/')[0]);
    return total + note;
  }, 0);

  const average_note = total_notes / messages.size;

  const embed = new discord.MessageEmbed()
    .setTitle('Moyenne des avis')
    .setDescription(`La moyenne des notes est de ${average_note.toFixed(1)}/20`)
    .setColor('#5865F2')
    .setTimestamp();

  const moyenne_channel = client.channels.cache.get('1081294505019461742'); // Remplace 'channel_id_here' par l'ID du salon où tu veux afficher la moyenne
  moyenne_channel.send({ embeds: [embed] });

  client.destroy();
});

client.login('TOKEN'); // Remplace 'token_here' par le token de ton bot Discord
