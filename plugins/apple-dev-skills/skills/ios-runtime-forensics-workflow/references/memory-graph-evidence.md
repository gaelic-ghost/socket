# Memory Graph Evidence

Drive the exact flow expected to release an object before capture. Record the object type, expected lifetime, action that should release it, simulator/app build, and capture point.

Start from app-owned types, then inspect the retaining chain rather than treating every live framework object as a leak. Re-capture the same flow after the smallest repair; report retained-object count and ownership-path changes separately from total process memory.
