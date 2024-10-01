const express = require('express');
const mysql = require('mysql');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());

const db = mysql.createConnection({
    host: 'mysql.railway.internal',  // Cambiado para usar el túnel SSH
    user: 'root',
    password: 'lDWLBIxYCbLnYZXYqQFYLkNrTJVgQnDM',
    database: 'railway',
    port: 3306
  });  

db.connect(err => {
  if (err) {
    console.error('Error conectando a la base de datos MySQL:', err);
    return;
  }
  console.log('Conectado a la base de datos MySQL');
});

app.get('/estado-juego', (req, res) => {
    const query = `
      SELECT voto 
      FROM votos 
      ORDER BY timestamp DESC 
      LIMIT 1
    `;
  
    db.query(query, (err, result) => {
      if (err) {
        console.error('Error en la consulta SQL:', err);
        return res.status(500).send("Error obteniendo las votaciones");
      }
  
      if (result.length > 0) {
        const ultimoVoto = result[0].voto;
  
        let estadoJuego = {
          direccion: ultimoVoto,
          mensaje: `El último voto fue ${ultimoVoto}`
        };
  
        res.json(estadoJuego);
      } else {
        // Si no hay votos, enviar un estado vacío o un mensaje predeterminado
        res.json({ mensaje: "No hay votos disponibles" });
      }
    });
  });
  

// API para actualizar el estado del juego
app.post('/actualizar-juego', (req, res) => {
  const { x, y } = req.body;

  if (x == null || y == null) {
    return res.status(400).send('Faltan coordenadas x o y');
  }

  const query = 'UPDATE estado_juego SET x = ?, y = ? WHERE id = 1';
  db.query(query, [x, y], (err, result) => {
    if (err) {
      console.error('Error actualizando el estado del juego:', err);
      return res.status(500).send('Error actualizando el estado del juego');
    }

    res.send('Estado del juego actualizado correctamente');
  });
});

// Iniciar el servidor
const PORT = process.env.PORT || 3306;
app.listen(PORT, () => {
  console.log(`Servidor corriendo en http://localhost:${PORT}`);
});
