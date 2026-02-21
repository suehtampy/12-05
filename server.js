// server.js
import express from "express";
import fetch from "node-fetch"; // npm i node-fetch
import cors from "cors";
import bodyParser from "body-parser";

const app = express();
const PORT = process.env.PORT || 3000;

// 🔹 Sua chave de API Gemini / OpenAI (somente aqui)
const API_KEY = "AQ.Ab8RN6IZW19NWxhH5yPt55RwTmWG2-v53v2sQSjCcNCGAYv-VQ";

app.use(cors());
app.use(bodyParser.json());
app.use(express.static("public"));

// Endpoint para processar resumo
app.post("/resumir", async (req, res) => {
  const { texto } = req.body;
  if (!texto || texto.trim() === "") return res.status(400).json({ error: "Texto vazio" });

  try {
    const response = await fetch("https://api.generative.ai/v1/models/text-bison-001:generate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${API_KEY}`
      },
      body: JSON.stringify({
        prompt: `Resuma o seguinte texto em poucas linhas mantendo a essência:\n\n${texto}`,
        temperature: 0.5,
        max_output_tokens: 300
      })
    });

    const data = await response.json();
    const resumo = data?.candidates?.[0]?.content || "❌ Não foi possível gerar resumo";
    res.json({ resumo });

  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Erro ao gerar resumo" });
  }
});

app.listen(PORT, () => console.log(`Servidor rodando em http://localhost:${PORT}`));
