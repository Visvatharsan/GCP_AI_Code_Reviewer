const { onRequest } = require("firebase-functions/v2/https");
const { defineSecret } = require("firebase-functions/params");
const { GoogleGenerativeAI } = require("@google/generative-ai");

const geminiApiKey = defineSecret("GEMINI_API_KEY");

exports.reviewCode = onRequest({ secrets: [geminiApiKey] }, async (req, res) => {
  const apiKey =
    process.env.FUNCTIONS_EMULATOR === "true" && process.env.GEMINI_API_KEY
      ? process.env.GEMINI_API_KEY
      : geminiApiKey.value();

  if (!apiKey) {
    res
      .status(500)
      .send("Missing GEMINI_API_KEY. Set it in your environment or secrets.");
    return;
  }

  const genAI = new GoogleGenerativeAI(apiKey);
  const code = req.body.code;
  const model = genAI.getGenerativeModel({ model: "gemini-2.5-flash-lite" });

  const prompt = `
  Review this code and provide your response as a valid JSON object strictly matching this format:
  {
    "issuesAndFixes": "A single string containing the explanation of bugs, security issues, and performance improvements.",
    "improvedCode": "A single string containing only the revised code, without markdown code blocks."
  }

  Code:
  ${code}
  `;

  const result = await model.generateContent(prompt);
  let responseText = result.response.text();
  
  // Remove markdown code block if present to ensure valid JSON
  responseText = responseText.replace(/```json/gi, '').replace(/```/g, '').trim();
  
  res.type('application/json').send(responseText);
});
