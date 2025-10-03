document.addEventListener('DOMContentLoaded', () => {
  const askBtn = document.getElementById('ask')
  const questionEl = document.getElementById('question')
  const authEl = document.getElementById('auth')
  const messagesEl = document.getElementById('messages')
  const quickQs = document.getElementById('quick-questions')

  function appendMessage(text, side = 'bot', meta = null) {
    const wrapper = document.createElement('div')
    wrapper.className = `message ${side}`

    const role = document.createElement('div')
    role.className = 'role'
    role.textContent = side === 'user' ? 'You' : 'Assistant'
    wrapper.appendChild(role)

    const bubble = document.createElement('div')
    bubble.className = 'bubble'
    bubble.textContent = text

    wrapper.appendChild(bubble)

    if (meta) {
      const metaEl = document.createElement('div')
      metaEl.className = 'meta'
      if (meta.files && meta.files.length) {
        const filesTitle = document.createElement('div')
        filesTitle.className = 'meta-title'
        filesTitle.textContent = 'Files used:'
        metaEl.appendChild(filesTitle)

        const ul = document.createElement('ul')
        meta.files.forEach(f => {
          const li = document.createElement('li')
          li.textContent = f
          ul.appendChild(li)
        })
        metaEl.appendChild(ul)
      }

      if (meta.file_search_text) {
        const fsTitle = document.createElement('div')
        fsTitle.className = 'meta-title'
        fsTitle.textContent = 'File search text:'
        metaEl.appendChild(fsTitle)

        const pre = document.createElement('pre')
        pre.textContent = meta.file_search_text
        metaEl.appendChild(pre)
      }

      wrapper.appendChild(metaEl)
    }

    messagesEl.appendChild(wrapper)
    messagesEl.scrollTop = messagesEl.scrollHeight
  }

  async function sendQuestion() {
    const q = questionEl.value
    const auth = authEl.value.trim()
    if (!q.trim()) return

    // append user message
    appendMessage(q.trim(), 'user')
    questionEl.value = ''

    // append bot placeholder
    appendMessage('Thinking...', 'bot')

    try {
      const res = await fetch('/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: q, auth_token: auth })
      })

      // remove the last bot placeholder
      const bots = messagesEl.querySelectorAll('.message.bot')
      const lastBot = bots[bots.length - 1]
      if (!res.ok) {
        const err = await res.json().catch(() => ({ error: res.statusText }))
        if (lastBot) lastBot.querySelector('.bubble').textContent = `Error: ${err.error || res.statusText}`
        return
      }

      const data = await res.json()
      if (lastBot) lastBot.querySelector('.bubble').textContent = data.answer || 'No answer returned.'

      // attach meta under the bot message
      if (lastBot && (data.files_used || data.file_search_text)) {
        const meta = { files: data.files_used || [], file_search_text: data.file_search_text }
        const metaEl = document.createElement('div')
        metaEl.className = 'meta'

        if (meta.files.length) {
          const filesTitle = document.createElement('div')
          filesTitle.className = 'meta-title'
          filesTitle.textContent = 'Files used:'
          metaEl.appendChild(filesTitle)

          const ul = document.createElement('ul')
          meta.files.forEach(f => {
            const li = document.createElement('li')
            li.textContent = f
            ul.appendChild(li)
          })
          metaEl.appendChild(ul)
        }

        if (meta.file_search_text) {
          const fsTitle = document.createElement('div')
          fsTitle.className = 'meta-title'
          fsTitle.textContent = 'File search text:'
          metaEl.appendChild(fsTitle)

          const pre = document.createElement('pre')
          pre.textContent = meta.file_search_text
          metaEl.appendChild(pre)
        }

        lastBot.appendChild(metaEl)
      }
    } catch (e) {
      const bots = messagesEl.querySelectorAll('.message.bot')
      const lastBot = bots[bots.length - 1]
      if (lastBot) lastBot.querySelector('.bubble').textContent = 'Network error: ' + e.message
    }
  }

  // wire quick question chips
  if (quickQs) {
    quickQs.addEventListener('click', (e) => {
      const btn = e.target.closest('.chip')
      if (!btn) return
      questionEl.value = btn.textContent
      // small delay so UI updates before sending
      setTimeout(() => sendQuestion(), 120)
    })
  }

  askBtn.addEventListener('click', sendQuestion)

  // Send on Enter, allow Shift+Enter for newline
  questionEl.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendQuestion()
    }
  })
})
