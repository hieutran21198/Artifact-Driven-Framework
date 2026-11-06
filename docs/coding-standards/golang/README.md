# Go

The Go coding standard for the services written in Go.

Read the [general coding standard](../general/README.md) first. It defines the
rule levels, the rule IDs, the precedence and the exception forms, and it holds
the rules that apply to every language.

This standard adds the Go mechanism and cites the general rule. It does not
repeat the general rule. The
[rule conventions](../general/README.md#rule-conventions) explain how rules are
chosen, cited and changed.

## Scope and assumptions

The scope is the same as the [General scope](../general/README.md#scope): Go
code in the structure of each service module that the architecture describes.
Generated code, `testdata/` and third-party code in `vendor/` are excluded.
Mark generated files with the standard header and do not edit them by hand.

Each service pins its Go release in its `go.mod`. Reassess compatibility
before upgrading.

## Toolchain and modules (GO-1xx)

| ID | Level | Rule |
| --- | --- | --- |
| GO-101 | MUST | Each service is one module. Do not add a second module or a `go.work` file inside a service. |
| GO-102 | MUST | Each module's `go` directive names the pinned toolchain release. |
| GO-104 | MUST NOT | Use `init()` for behavior with side effects. Wire dependencies in `main` or in a constructor. |
| GO-105 | MUST | Keep module files tidy. `go mod tidy` leaves no diff. |
| GO-106 | MUST NOT | Use `replace` directives except for a temporary local fix that the same change removes. |

## Packages and layout (GO-2xx)

| ID | Level | Rule |
| --- | --- | --- |
| GO-202 | MUST | Define an interface in the package that consumes it, not in the package that implements it. |
| GO-204 | MUST | Keep code that no other module imports under `internal/`. |
| GO-206 | MUST | `cmd/` holds process wiring only: flags, configuration, construction and start. |
| GO-207 | MUST | A package name is lowercase, one word, and matches its directory name. |

## API surface (GO-3xx)

| ID | Level | Rule |
| --- | --- | --- |
| GO-301 | MUST | Accept interfaces and return concrete types. |
| GO-303 | SHOULD | Use functional options only when a second caller needs the variation. Until then, use explicit parameters. |

`GO-301` has one exception: return an interface when the implementation type is
an internal detail that callers must not name. State the reason in a comment.

## Errors (GO-4xx)

| ID | Level | Rule |
| --- | --- | --- |
| GO-401 | MUST | Wrap a returned error with `fmt.Errorf("...: %w", err)` so that `errors.Is` and `errors.As` still match it. |
| GO-402 | MUST | Match an error with `errors.Is` or `errors.As`, never with a string comparison. |
| GO-404 | MUST NOT | Use `panic` for a state that the code can reach, such as invalid input. |
| GO-405 | MUST | Define a sentinel or typed error only when a caller must branch on it. |
| GO-406 | MUST | An error message is lowercase and has no trailing punctuation. |

```go
// Wrong: the caller cannot match the cause with errors.Is.
if err != nil {
    return errors.New("save failed")
}

// Right: add the operation and keep the cause in the chain.
if err := store.Save(ctx, order); err != nil {
    return fmt.Errorf("save order %s: %w", order.ID, err)
}
```

`GEN-304` owns the choice of the layer that adds the operation context.
`GEN-301` owns the requirement to handle or propagate the failure.
GO-401 preserves the cause only when it is safe to expose. Never propagate a
cause that contains a secret or violates the caller's error contract. Translate
such failures to a safe typed/sentinel error; record and review any necessary
GO-401 exception under the General conventions. Do not log the sensitive cause
as a workaround (GEN-604).

## Concurrency (GO-5xx)

| ID | Level | Rule |
| --- | --- | --- |
| GO-501 | MUST | Pass `context.Context` as the first parameter. Never store it in a struct. |
| GO-502 | MUST | Every goroutine has an owner, a stop condition and a wait. |
| GO-503 | MUST | Use `errgroup` to run a group of related goroutines and to collect their errors. |
| GO-504 | MUST | Bound the concurrency for an input whose size the service does not control. |
| GO-505 | SHOULD | Use a channel to transfer ownership and a mutex to protect shared state. |
| GO-507 | MUST | Protect every write to shared state with a mutex or an atomic type. A map write from two goroutines without synchronization is a defect. |

`GEN-104` owns the requirement to minimize shared mutable state.

```go
// Wrong: the context is stored, so its lifetime is not the lifetime of the call.
type Client struct {
    ctx context.Context
}
```

The right form passes `ctx` as the first parameter of each method. The caller
then controls the deadline and the cancellation. `GEN-503` states that
requirement; GO-501 states the Go form of it.

```go
// Wrong: no owner, no stop condition and no wait.
go func() { _ = poll() }()

// Right: the parent waits, and cancellation stops the work.
g, ctx := errgroup.WithContext(ctx)
g.Go(func() error { return poll(ctx) })
return g.Wait()
```

## Lifetimes and shutdown (GO-6xx)

| ID | Level | Rule |
| --- | --- | --- |
| GO-602 | MUST | The local HTTP server sets read, write and idle timeouts, and shuts down gracefully on a signal. On a serverless runtime, the runtime owns the server lifetime. |
| GO-603 | MUST | Close a resource in the function that opened it, with a deferred call after the error check. |
| GO-605 | MUST | Do not replace the caller's context with `context.Background()` inside a request path. |

`GEN-502` owns the timeout requirement and `GEN-505` owns the release
requirement. GO-602, GO-603 and GO-605 state the Go forms.

```go
conn, err := pool.Acquire(ctx)
if err != nil {
    return fmt.Errorf("acquire connection: %w", err)
}
defer conn.Release()
```

```go
srv := &http.Server{
    Addr:              addr,
    Handler:           handler,
    ReadHeaderTimeout: 5 * time.Second,
    ReadTimeout:       15 * time.Second,
    WriteTimeout:      15 * time.Second,
    IdleTimeout:       60 * time.Second,
}

ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
defer stop()

errs := make(chan error, 1)
go func() {
    if err := srv.ListenAndServe(); err != nil && !errors.Is(err, http.ErrServerClosed) {
        errs <- err
    }
}()

select {
case err := <-errs:
    return err
case <-ctx.Done():
}

shutdownCtx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
defer cancel()
return srv.Shutdown(shutdownCtx)
```

## Observability (GO-7xx)

| ID | Level | Rule |
| --- | --- | --- |
| GO-701 | MUST | Log with `log/slog` and the `Context` variants, so that a record carries the request scope. |

`GEN-601` to `GEN-605` own the content rules: structured keys, no console
output, one record per cause, no sensitive data and request correlation.

```go
// Wrong
fmt.Printf("order %s saved\n", orderID)

// Right
slog.InfoContext(ctx, "order saved", "order_id", orderID)
```

## Security (GO-8xx)

| ID | Level | Rule |
| --- | --- | --- |
| GO-803 | MUST NOT | Set `InsecureSkipVerify` on a TLS configuration. |
| GO-805 | MUST | Keep `govulncheck ./...` clean. |

`GEN-405` owns the verification requirement and `GEN-804` owns the
vulnerability requirement. GO-803 and GO-805 state the Go forms.

## Tests (GO-9xx)

| ID | Level | Rule |
| --- | --- | --- |
| GO-901 | MUST | Write table-driven tests with named subtests. |
| GO-902 | MUST | Call `t.Helper` in a test helper and register cleanup with `t.Cleanup`. |
| GO-903 | SHOULD | Prefer a small hand-written fake to a generated mock. |
| GO-904 | MUST | Put an integration test behind a build tag. |
| GO-906 | MUST | Run the test gate with `-race`. Mark a test that cannot use the race detector with a recorded reason. |

`GEN-701` to `GEN-706` own the test requirements. GO-901 to GO-904 and GO-906
state the Go forms.

```go
func TestParsePort(t *testing.T) {
    tests := map[string]struct {
        in      string
        want    int
        wantErr bool
    }{
        "valid":   {in: "8080", want: 8080},
        "zero":    {in: "0", want: 0},
        "too big": {in: "70000", wantErr: true},
        "empty":   {in: "", wantErr: true},
    }

    for name, tt := range tests {
        t.Run(name, func(t *testing.T) {
            t.Parallel()

            got, err := ParsePort(tt.in)
            if tt.wantErr {
                if err == nil {
                    t.Fatalf("ParsePort(%q) = %d, want error", tt.in, got)
                }
                return
            }
            if err != nil {
                t.Fatalf("ParsePort(%q) returned error: %v", tt.in, err)
            }
            if got != tt.want {
                t.Fatalf("ParsePort(%q) = %d, want %d", tt.in, got, tt.want)
            }
        })
    }
}
```

## Clarity (GO-10xx)

| ID | Level | Rule |
| --- | --- | --- |
| GO-1001 | MUST | Keep the code formatted with `gofmt`. |
| GO-1002 | MUST | Avoid stutter between a package name and its identifiers, as in `order.OrderService`. |
| GO-1003 | MUST | An exported identifier has a doc comment that starts with its name. |
| GO-1004 | SHOULD | Use a type parameter only to remove real duplication. |

`GEN-201` owns the naming requirement and `GEN-203` owns the documentation
requirement. GO-1002 and GO-1003 state the Go forms.

## Gates

Run these checks from the root of each service module. They describe the target gates;
a service CI may not run all of them yet. GEN-1001 to GEN-1003 govern merge, local/CI
parity and deliberate skips. Pin compatible tool versions before use.

| Gate | Method | Relevant rules |
| --- | --- | --- |
| Formatting | `gofmt -l .` prints nothing | GO-1001 |
| Vet | `go vet ./...` | Type and format-string checks |
| Static analysis | `staticcheck ./...`, configured for the selected Go version | Review diagnostic coverage; no one-to-one enforcement of prose rules is assumed |
| Tests | `go test -race ./...`; run integration-tagged tests separately against their dependencies | GO-901 to GO-904, GO-906; GEN-704 |
| Vulnerabilities | `govulncheck ./...` | GO-805 |
| Modules | In a disposable working copy, `go mod tidy` leaves no diff | GO-105 |
| Build | `go build ./...` | Compilation |

A service may compose these checks into a `task` command. Verify what each tool checks and record gaps;
a passing tool does not prove every rule or human review is satisfied.

## Exceptions register

`GEN-1101` and `GEN-1102` own the exception rules. This table is the register
for the Go rules.

| Rule | Scope | Reason | Owner | Review date |
| --- | --- | --- | --- | --- |
| None | — | — | — | — |

## Local use

Read the [project instructions](../../../AGENTS.md) and the
[General standard](../general/README.md) first. A change to this standard is its
own reviewed pull request. Keep run results, progress and discussion on the
issue or pull request.

Return to [coding standards](../README.md).
