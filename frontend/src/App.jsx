import { Tldraw } from "tldraw"
import "tldraw/tldraw.css"
import { useEffect, useRef, useState } from "react"

export default function App() {

  const editorRef = useRef(null)
  const socketRef = useRef(null)

  const [sessionActive, setSessionActive] = useState(false)

  const client_id = "Saviour"

  useEffect(() => {

    const socket = new WebSocket(
      `ws://localhost:8000/ws/opentutor/${client_id}`
      //`ws://localhost:8000/ws/opentutor/${client_id}`
    )

    socketRef.current = socket

    socket.onopen = () => {
      console.log("Connected to backend WebSocket")
    }

    socket.onmessage = (event) => {

      const msg = JSON.parse(event.data)
      console.log("Received:", msg)

      const editor = editorRef.current
      if (!editor) return

      const data = msg.data || {}

      switch (msg.action) {

        case "draw_shape":

          editor.createShape({
            id: data.id,
            type: "geo",
            x: data.x,
            y: data.y,
            props: {
              geo: data.shape,
              w: data.width || 120,
              h: data.height || 120
            }
          })

          break


        case "write_text":

          editor.createShape({
            id: data.id,
            type: "text",
            x: data.x,
            y: data.y,
            props: {
              richText: {
                type: "doc",
                content: [
                  {
                    type: "paragraph",
                    content: [
                      {
                        type: "text",
                        text: data.text
                      }
                    ]
                  }
                ]
              }
            }
          })

          break


        case "delete_shape":

          editor.deleteShapes([data.shapeId])

          break


        case "clear_board":

          const shapes = editor.getCurrentPageShapes()

          editor.deleteShapes(
            shapes.map(shape => shape.id)
          )

          break


        case "move_shape": {

          const shape = editor.getShape(data.shapeId)

          if (!shape) {
            console.log("Shape not found:", data.shapeId)
            return
          }

          editor.updateShape({
            ...shape,
            x: data.x,
            y: data.y
          })

          break
        }


        case "resize_item": {

          const shape = editor.getShape(data.shapeId)

          if (!shape) return

          editor.updateShape({
            ...shape,
            props: {
              ...shape.props,
              w: data.width,
              h: data.height
            }
          })

          break
        }


        // draw a straight line
        case "draw_line": {

          editor.createShape({
            id: data.id,
            type: "line",
            x: data.x,
            y: data.y,
            props: {
              points: [
                { x: 0, y: 0 },
                { x: data.x2 - data.x, y: data.y2 - data.y }
              ]
            }
          })

          break
        }


// draw curve lines
        case "draw_curve": {

          editor.createShape({
            id: data.id,
            type: "draw",
            x: data.x,
            y: data.y,
            props: {
              segments: [
                {
                  type: "free",
                  points: data.points
                }
              ]
            }
          })

          break
        }



        default:
          console.log("Unknown action:", msg.action)
      }

    }

    return () => {
      socket.close()
    }

  }, [])


  function startSession() {

    const socket = socketRef.current

    if (!socket || socket.readyState !== WebSocket.OPEN) {
      console.log("WebSocket not connected")
      return
    }

    socket.send(JSON.stringify({
      action: "start_session"
    }))

    setSessionActive(true)
  }


  function endSession() {

    const socket = socketRef.current

    if (!socket || socket.readyState !== WebSocket.OPEN) {
      console.log("WebSocket not connected")
      return
    }

    socket.send(JSON.stringify({
      action: "end_session"
    }))

    setSessionActive(false)
  }


  return (

    <div style={{ position: "fixed", inset: 0 }}>

      <Tldraw
        onMount={(editor) => {
          editorRef.current = editor
        }}
      />

      <div
        style={{
          position: "absolute",
          bottom: 30,
          left: "50%",
          transform: "translateX(-50%)",
          zIndex: 1000
        }}
      >

        {!sessionActive ? (

          <button
            onClick={startSession}
            style={{
              padding: "20px 40px",
              fontSize: "16px",
              borderRadius: "8px",
              border: "none",
              background: "#2ecc71",
              color: "white",
              cursor: "pointer"
            }}
          >
            Start Session
          </button>

        ) : (

          <button
            onClick={endSession}
            style={{
              padding: "20px 40px",
              fontSize: "16px",
              borderRadius: "8px",
              border: "none",
              background: "#e74c3c",
              color: "white",
              cursor: "pointer"
            }}
          >
            End Session
          </button>

        )}

      </div>

    </div>
  )

}
