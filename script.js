import { GoogleGenerativeAI } from "https://esm.run/@google/generative-ai";

// Contador de caracteres simples
document.getElementById('inputText').addEventListener('input', (e) => {
    document.getElementById('charCount').innerText = `${e.target.value.length} caracteres`;
});

// Função principal que roda ao clicar no botão
window.processar = async function() {
    const key = document.getElementById('AIzaSyAPi1-sZfA_Ilp2qVqkvQ5mgk7yvfe8g_E').value;
    const text = document.getElementById('inputText').value;
    const btn = document.getElementById('btnGo');
    const outputDiv = document.getElementById('resultContainer');
    const outputText = document.getElementById('outputText');
    const loading = document.getElementById('loading');

    if (!key) return alert("Por favor, insira sua API Key do Gemini.");
    if (!text || text.length < 20) return alert("O texto parece muito curto para resumir.");

    try {
        btn.disabled = true;
        loading.classList.remove('hidden');
        outputDiv.classList.add('hidden');

        // Inicializa a IA
        const genAI = new GoogleGenerativeAI(key);
        const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });

        const prompt = `Você é um assistente de produtividade. Analise o texto abaixo e retorne um resumo estruturado:
        1. O QUE É: (Uma frase resumindo o assunto)
        2. PONTOS CHAVE: (Máximo 4 tópicos com os detalhes mais importantes)
        3. AÇÃO NECESSÁRIA: (Se houver datas ou tarefas, liste aqui. Se não, diga 'Apenas informativo')
        
        Use linguagem simples e direta. Texto: ${text}`;

        const result = await model.generateContent(prompt);
        const response = await result.response;
        
        // Exibe o resultado
        outputText.innerText = response.text();
        outputDiv.classList.remove('hidden');
    } catch (error) {
        console.error(error);
        alert("Erro: Verifique se sua chave está correta ou se o texto é suportado.");
    } finally {
        btn.disabled = false;
        loading.classList.add('hidden');
    }
}

// Função para copiar o texto
window.copyText = function() {
    const text = document.getElementById('outputText').innerText;
    navigator.clipboard.writeText(text);
    alert("Copiado para a área de transferência!");
}
