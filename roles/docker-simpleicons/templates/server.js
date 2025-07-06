import express from 'express';
import * as icons from 'simple-icons';
import sharp from 'sharp';

const app = express();
const port = process.env.PORT || 3000;

// Helper: turn 'nextcloud' → 'siNextcloud'
function getExportName(slug) {
  return 'si' + slug
    .split('-')
    .map(part => part[0].toUpperCase() + part.slice(1))
    .join('');
}

// GET /icons/:slug.svg
app.get('/icons/:slug.svg', (req, res) => {
  const slug = req.params.slug.toLowerCase();
  const exportName = getExportName(slug);
  const icon = icons[exportName];

  if (!icon) {
    return res.status(404).send('Icon not found');
  }

  res.type('image/svg+xml').send(icon.svg);
});

// GET /icons/:slug.png?size=...
app.get('/icons/:slug.png', async (req, res) => {
  const slug = req.params.slug.toLowerCase();
  const size = parseInt(req.query.size, 10) || 128;
  const exportName = getExportName(slug);
  const icon = icons[exportName];

  if (!icon) {
    return res.status(404).send('Icon not found');
  }

  try {
    const png = await sharp(Buffer.from(icon.svg))
      .resize(size, size)
      .png()
      .toBuffer();

    res.type('image/png').send(png);
  } catch (err) {
    console.error('PNG generation error:', err);
    res.status(500).send('PNG generation error');
  }
});

app.listen(port, () => {
  console.log(`Simple-Icons server listening at http://0.0.0.0:${port}`);
});
