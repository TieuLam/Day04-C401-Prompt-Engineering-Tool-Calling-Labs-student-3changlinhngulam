import { NextResponse } from 'next/server';
import { execFile } from 'child_process';
import { promisify } from 'util';
import path from 'path';

const execFileAsync = promisify(execFile);

export async function POST(req: Request) {
  try {
    const { query } = await req.json();

    if (!query) {
      return NextResponse.json({ error: 'Query is required' }, { status: 400 });
    }

    const starterDir = path.resolve(process.cwd(), '..');
    const pythonExe = path.join(starterDir, '.venv', 'Scripts', 'python.exe');
    const scriptPath = path.join(starterDir, 'run_single.py');
    
    // Execute the python script with the query as an argument
    const { stdout } = await execFileAsync(pythonExe, [scriptPath, query], { cwd: starterDir });

    try {
      // Find the first { in case there are print statements before the JSON
      const jsonStart = stdout.indexOf('{');
      const jsonStr = jsonStart >= 0 ? stdout.substring(jsonStart) : stdout;
      const result = JSON.parse(jsonStr);
      return NextResponse.json(result);
    } catch (parseError) {
      console.error("Failed to parse JSON:", stdout);
      return NextResponse.json({ error: 'Failed to parse agent response', details: stdout }, { status: 500 });
    }
  } catch (error: any) {
    console.error("Error executing agent:", error);
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}
