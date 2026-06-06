<script>
  import { onMount } from 'svelte'
  let health = null
  let error = null

  const apiBase = import.meta.env.VITE_API_URL || 'http://localhost:8000'

  onMount(async () => {
    try {
      const res = await fetch(`${apiBase}/health`)
      if (!res.ok) throw new Error(`HTTP ${res.status}`)
      health = await res.json()
    } catch (e) {
      error = e.message
    }
  })
</script>

<main>
  <h1>Viral Shorts — Frontend (Svelte)</h1>

  {#if health}
    <section>
      <h2>API Health</h2>
      <pre>{JSON.stringify(health, null, 2)}</pre>
    </section>
  {:else if error}
    <section>
      <h2>Error</h2>
      <p>{error}</p>
    </section>
  {:else}
    <p>Loading API status…</p>
  {/if}

  <section>
    <h2>Notes</h2>
    <ul>
      <li>This simple SPA demonstrates fetching the backend health endpoint.</li>
      <li>Set VITE_API_URL to point at the API (default: http://localhost:8000).</li>
    </ul>
  </section>
</main>

<style>
  main { font-family: system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial; padding: 2rem; }
  pre { background:#f6f8fa; padding:1rem; border-radius:6px }
</style>
