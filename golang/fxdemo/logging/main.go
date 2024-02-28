package main

import (
	"go.uber.org/fx"
	"go.uber.org/fx/fxevent"
	"go.uber.org/zap"
	"log/slog"
	"os"
)

func LoggerModule(name string, opts ...fx.Option) fx.Option {
	return fx.Module(name, fx.Options(opts...),
		fx.Decorate(func(logger *slog.Logger) *slog.Logger {
			return logger.With("module", name)
		}),
	)
}

func main() {
	module1 := LoggerModule("mod1",
		fx.Invoke(func(logger *slog.Logger) {
			logger.Info("init")
		}),
	)

	module2 := LoggerModule("mod2",
		fx.Invoke(func(logger *slog.Logger) {
			logger.Info("init")
		}),
	)

	module := fx.Module("main",
		module1,
		module2,
		fx.WithLogger(func(logger *slog.Logger) fxevent.Logger {
			return &fxevent.ZapLogger{Logger: zap.NewExample()}
		}),
		fx.Provide(func() *slog.Logger {
			return slog.New(slog.NewJSONHandler(os.Stdout, nil))
		}),
		fx.Invoke(func(logger *slog.Logger) {
			logger.Info("init")
		}),
	)

	fx.New(module).Run()
}
