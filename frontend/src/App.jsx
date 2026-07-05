import React, { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import axios from 'axios'

const API = 'http://localhost:8002'

export default function App() {
  const [tab, setTab] = useState('chat')
  const [question, setQuestion] = useState('')
  const [answer, setAnswer] = useState(null)
  const qc = useQueryClient()

  const { data: docs } = useQuery({
    queryKey: ['docs'],
    queryFn: () => axios.get(`${API}/list-documents`).then(r => r.data),
  })

  const uploadMut = useMutation({
    mutationFn: files => {
      const fd = new FormData()
      files.forEach(f => fd.append('files', f))
      return axios.post(`${API}/upload`, fd)
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ['docs'] }),
  })

  const queryMut = useMutation({
    mutationFn: q => axios.post(`${API}/query`, { question: q }).then(r => r.data),
  })

  const deleteMut = useMutation({
    mutationFn: id => axios.delete(`${API}/delete-document/${id}`),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['docs'] }),
  })

  const handleAsk = () => {
    if (!question.trim()) return
    queryMut.mutate(question, { onSuccess: setAnswer })
  }

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-3xl font-bold text-center text-gray-800 mb-8">Personal Knowledge Base</h1>

      <div className="flex gap-2 mb-6">
        <button onClick={() => setTab('chat')} className={`px-4 py-2 rounded-lg ${tab === 'chat' ? 'bg-blue-600 text-white' : 'bg-gray-200'}`}>Chat</button>
        <button onClick={() => setTab('library')} className={`px-4 py-2 rounded-lg ${tab === 'library' ? 'bg-blue-600 text-white' : 'bg-gray-200'}`}>Library</button>
      </div>

      {tab === 'chat' && <>
        <div className="flex gap-2 mb-4">
          <input value={question} onChange={e => setQuestion(e.target.value)}
            placeholder="Ask a question about your documents..."
            className="flex-1 p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400" />
          <button onClick={handleAsk} disabled={queryMut.isPending}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 disabled:opacity-50">
            {queryMut.isPending ? 'Thinking...' : 'Ask'}
          </button>
        </div>

        {(answer || queryMut.isPending) && <div className="bg-white p-6 rounded-lg shadow">
          {queryMut.isPending ? <p className="text-gray-500 animate-pulse">Thinking...</p> : <>
            <div className="prose max-w-none text-gray-700 mb-4 whitespace-pre-wrap">{answer.answer}</div>
            {answer.sources?.length > 0 && <div className="flex gap-2 flex-wrap">
              {answer.sources.map((s, i) => (
                <span key={i} className="px-2 py-1 bg-gray-100 text-gray-600 text-sm rounded-full">
                  {s.filename} p.{s.page}
                </span>
              ))}
            </div>}
          </>}
        </div>}
      </>}

      {tab === 'library' && <>
        <div className="mb-4">
          <input type="file" multiple accept=".pdf,.docx,.txt,.md,.png,.jpg,.jpeg" onChange={e => {
            if (e.target.files.length) uploadMut.mutate([...e.target.files])
          }} className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100" />
        </div>

        <div className="space-y-2">
          {docs?.map(d => (
            <div key={d.id} className="flex items-center justify-between bg-white p-3 rounded-lg shadow">
              <span className="text-gray-700">{d.filename}</span>
              <button onClick={() => deleteMut.mutate(d.id)} className="text-red-500 hover:text-red-700 text-sm">Delete</button>
            </div>
          ))}
          {docs?.length === 0 && <p className="text-gray-500 text-center py-8">No documents yet. Upload some!</p>}
        </div>
      </>}
    </div>
  )
}
