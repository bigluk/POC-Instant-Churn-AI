import { useState, useRef } from "react";
import { Card, Button, Form, InputGroup, Badge, Spinner } from "react-bootstrap";
import { ChatDots, Dash, Fullscreen, X } from "react-bootstrap-icons";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

type Message = {
    id: number;
    sender: "user" | "operator";
    text: string;
    time: string;
};

const BankChat: React.FC = () => {
    const [messages, setMessages] = useState<Message[]>([
        {
            id: 1,
            sender: "operator",
            text: "Hi, how can I help you today?",
            time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
        },
    ]);

    const [input, setInput] = useState("");
    const [isOpen, setIsOpen] = useState(false);
    const [isFullscreen, setIsFullscreen] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const exitFullscreen = () => setIsFullscreen(false);

    const [position, setPosition] = useState({ x: 0, y: 0 });
    const offset = useRef({ x: 0, y: 0 });
    const isDragging = useRef(false);

    const threadIdRef = useRef<string | null>(null);

    const handleSend = async () => {
        if (!input.trim()) return;

        const newMessage: Message = {
            id: Date.now(),
            sender: "user",
            text: input,
            time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
        };

        setMessages((prev) => [...prev, newMessage]);
        const userInput = input;
        setInput("");

        setIsLoading(true); // show spinner

        try {
            const body = {
                projectId: 1,
                question: userInput,
                threadId: threadIdRef.current || undefined,
            };

            const response = await fetch("/api/ask-to-ai", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(body),
            });

            const data = await response.json();
            threadIdRef.current = data.threadId;

            const operatorMessage: Message = {
                id: data.id,
                sender: "operator",
                text: data.explanation?.replace(/\\n/g, "\n") ??
                    data.summary?.replace(/\\n/g, "\n") ??
                    "No response received",
                time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
            };

            setMessages((prev) => [...prev, operatorMessage]);
        } catch (err) {
            console.error("Errore API:", err);
            const errorMessage: Message = {
                id: Date.now() + 1,
                sender: "operator",
                text: "An error occurred, please try again later.",
                time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
            };
            setMessages((prev) => [...prev, errorMessage]);
        } finally {
            setIsLoading(false);
        }
    };

    const onMouseDown = (e: React.MouseEvent) => {
        if (isFullscreen) return;
        isDragging.current = true;
        offset.current = { x: e.clientX - position.x, y: e.clientY - position.y };
        window.addEventListener("mousemove", onMouseMove);
        window.addEventListener("mouseup", onMouseUp);
    };
    const onMouseMove = (e: MouseEvent) => {
        if (!isDragging.current) return;
        setPosition({ x: e.clientX - offset.current.x, y: e.clientY - offset.current.y });
    };
    const onMouseUp = () => {
        isDragging.current = false;
        window.removeEventListener("mousemove", onMouseMove);
        window.removeEventListener("mouseup", onMouseUp);
    };

    return (
        <>
            {!isOpen && (
                <Button
                    variant="success"
                    className="rounded-circle shadow-lg position-fixed"
                    style={{ bottom: 24, right: 24, width: 60, height: 60, zIndex: 2000 }}
                    onClick={() => setIsOpen(true)}
                >
                    <ChatDots size={28} />
                </Button>
            )}

            {isOpen && (
                <div
                    className="position-fixed"
                    style={{
                        right: isFullscreen ? 0 : 10,
                        bottom: isFullscreen ? 0 : 10,
                        left: isFullscreen ? 0 : "auto",
                        transform: isFullscreen ? "none" : `translate(${position.x}px, ${position.y}px)`,
                        transition: isDragging.current ? "none" : "transform 0.3s ease, opacity 0.3s ease",
                        zIndex: 1500,
                    }}
                >
                    <Card
                        style={{
                            width: isFullscreen ? "100vw" : 400,
                            height: isFullscreen ? "100vh" : "auto",
                            maxHeight: "87vh",
                            border: "none",
                            borderRadius: "0"
                        }}
                        className="shadow-lg"
                    >
                        <Card.Header
                            onMouseDown={onMouseDown}
                            className="bg-success text-white d-flex justify-content-between align-items-center"
                            style={{ cursor: isFullscreen ? "default" : "move" }}
                        >
                            <div>
                                <strong>Wren AI</strong>
                                <div className="small">
                                    <Badge bg="danger" className="me-1">Online</Badge>
                                    AI Agent
                                </div>
                            </div>

                            <div className="d-flex gap-2">
                                {isFullscreen ? (
                                    <Button size="sm" variant="success" onClick={exitFullscreen}>
                                        <Dash className="fs-6" />
                                    </Button>
                                ) : (
                                    <Button size="sm" variant="success" onClick={() => setIsFullscreen(true)}>
                                        <Fullscreen className="fs-6" />
                                    </Button>
                                )}
                                <Button size="sm" variant="danger" onClick={() => setIsOpen(false)}>
                                    <X className="fs-6" />
                                </Button>
                            </div>
                        </Card.Header>

                        <Card.Body
                            style={{
                                height: isFullscreen ? "calc(100vh - 140px)" : 320,
                                overflowY: "auto",
                                background: "#f8f9fa",
                            }}
                        >
                            {messages.map((msg) => (
                                <div
                                    key={msg.id}
                                    className={`d-flex mb-3 ${msg.sender === "user" ? "justify-content-end" : "justify-content-start"}`}
                                >
                                    <div
                                        className={`p-3 rounded-4 ${msg.sender === "user" ? "bg-success text-white" : "bg-white border"}`}
                                        style={{ maxWidth: "75%" }}
                                    >
                                        <div className="chat-message">
                                            <ReactMarkdown remarkPlugins={[remarkGfm]}>
                                                {msg.text}
                                            </ReactMarkdown>
                                        </div>
                                        <div className="text-end small opacity-75 mt-1">{msg.time}</div>
                                    </div>
                                </div>
                            ))}

                            {/* Spinner loading */}
                            {isLoading && (
                                <div className="d-flex justify-content-start align-items-center mb-2">
                                    <Spinner animation="border" size="sm" className="me-2" />
                                    <div className="small text-muted">Processing your request...</div>
                                </div>
                            )}
                        </Card.Body>

                        <Card.Footer className="bg-white border-top p-0">
                            <InputGroup className="w-100 mt-2">
                                <Form.Control
                                    placeholder="Ask a question..."
                                    value={input} onChange={(e) => setInput(e.target.value)}
                                    onKeyDown={(e) => e.key === "Enter" && handleSend()}
                                    disabled={isLoading} // disable input during loading
                                />
                                <Button variant="success" onClick={handleSend} disabled={isLoading}>Send</Button>
                            </InputGroup>
                        </Card.Footer>
                    </Card>
                </div>
            )}
        </>
    );
};

export default BankChat;