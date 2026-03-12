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
  Review this code and give:
  - Bugs
  - Security issues
  - Performance improvements

  Code:
  ${code}
  `;

  const result = await model.generateContent(prompt);
  res.send(result.response.text());
});
