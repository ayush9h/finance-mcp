package handler

import (
	"context"
	"crypto/subtle"
	"net/http"

	"github.com/modelcontextprotocol/go-sdk/auth"
)

func TokenVerifier(token string) auth.TokenVerifier {
	expected := []byte(token)

	return func(_ context.Context, token string, _ *http.Request) (*auth.TokenInfo, error) {

		// comparing the lengths of the tokens, returns 1 if equal and 0 otherwise
		if subtle.ConstantTimeCompare([]byte(token), expected) != 1 {
			return nil, auth.ErrInvalidToken
		}

		return &auth.TokenInfo{}, nil
	}
}
