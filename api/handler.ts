import type { VercelRequest, VercelResponse } from '@vercel/node';

export default function handler(
  request: VercelRequest,
  response: VercelResponse,
) {
  response.status(200).json({
    body: request.body,
    query: request.query,
    cookies: request.cookies,
    env: process.env.TEST_SECRET,
    something_else: `Hi ${process.env.LANG}, ${process.env.SHELL}, ${process.env.TEST_SECRET}`
  });
}