const { v2: cloudinary } = require('cloudinary');

console.log("☁️ CLOUDINARY:");
console.log("CLOUD NAME:", process.env.CLOUDINARY_CLOUD_NAME);
console.log("API KEY:", process.env.CLOUDINARY_API_KEY ? "OK" : "NÃO ENCONTRADA");
console.log("API SECRET:", process.env.CLOUDINARY_API_SECRET ? "OK" : "NÃO ENCONTRADA");

cloudinary.config({
  cloud_name: process.env.CLOUDINARY_CLOUD_NAME,
  api_key: process.env.CLOUDINARY_API_KEY,
  api_secret: process.env.CLOUDINARY_API_SECRET,
});

module.exports = cloudinary;