import { PYTHON_API_URL } from "$env/static/private";

export async function POST({ request }) {
  const formData = await request.formData();

  // Forward to Python server (internal network only)
  const response = await fetch(`${PYTHON_API_URL}/process-batch`, {
    method: "POST",
    body: formData,
  });

  return new Response(await response.text(), {
    status: response.status,
    headers: { "Content-Type": "application/json" },
  });
}
