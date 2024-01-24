package main

import (
	"context"
	"fmt"
	"io"
	"log/slog"
	"net"
	"net/http"
	"os"

	"go.uber.org/fx"
)

func main() {
	fx.New(
		fx.Provide(
			NewHttpServer,
			fx.Annotate(
				NewServeMux,
				fx.ParamTags(`group:"routes"`),
			),
			AsRoute(NewEchoHandler),
			AsRoute(NewHelloHandler),
			NewLogger,
		),
		fx.Invoke(func(*http.Server) {}),
	).Run()
}

func AsRoute(f any) any {
	return fx.Annotate(
		f,
		fx.As(new(Route)),
		fx.ResultTags(`group:"routes"`),
	)
}

func NewHttpServer(lc fx.Lifecycle, mux *http.ServeMux, log *slog.Logger) *http.Server {
	srv := &http.Server{
		Addr:    ":8080",
		Handler: mux,
	}

	lc.Append(fx.Hook{
		OnStart: func(ctx context.Context) error {
			ln, err := net.Listen("tcp", srv.Addr)
			if err != nil {
				return nil
			}
			log.Info("Starting HTTP server", slog.String("addr", srv.Addr))
			go srv.Serve(ln)
			return nil
		},
		OnStop: func(ctx context.Context) error {
			log.Info("Stoping HTTP server", slog.String("addr", srv.Addr))
			return srv.Shutdown(ctx)
		},
	})

	return srv
}

func NewLogger() *slog.Logger {
	return slog.New(slog.NewJSONHandler(os.Stdout, nil))
}

func NewServeMux(routes []Route) *http.ServeMux {
	mux := http.NewServeMux()
	for _, route := range routes {
		mux.Handle(route.Pattern(), route)
	}
	return mux
}

type EchoHandler struct {
	log *slog.Logger
}

func NewEchoHandler(log *slog.Logger) *EchoHandler {
	return &EchoHandler{log: log}
}

func (h *EchoHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	if _, err := io.Copy(w, r.Body); err != nil {
		h.log.Warn("Failed to handle request", "my_error", err.Error())
	}
}

func (*EchoHandler) Pattern() string {
	return "/echo"
}

type Route interface {
	http.Handler
	Pattern() string
}

type HelloHandler struct {
	log *slog.Logger
}

func NewHelloHandler(log *slog.Logger) *HelloHandler {
	return &HelloHandler{log: log}
}

func (*HelloHandler) Pattern() string {
	return "/hello"
}

func (h *HelloHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	body, err := io.ReadAll(r.Body)
	if err != nil {
		h.log.Error("Failed to read request", "err1", err.Error())
		http.Error(w, "My Internal server error", http.StatusInternalServerError)
		return
	}

	if _, err := fmt.Fprintf(w, "Hello, %s\n", body); err != nil {
		h.log.Error("Failed to read request", "err2", err.Error())
		http.Error(w, "My Internal server error", http.StatusInternalServerError)
		return
	}
}
