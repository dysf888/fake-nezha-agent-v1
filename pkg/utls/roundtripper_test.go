package utls_test

import (
	"net/http"
	"os"
	"testing"

	utls "github.com/refraction-networking/utls"

	"github.com/dysf888/fake-nezha-agent-v1/pkg/util"
	utlsx "github.com/dysf888/fake-nezha-agent-v1/pkg/utls"
)

const url = "https://www.patreon.com/login"

func TestCloudflareDetection(t *testing.T) {
	if ci := os.Getenv("CI"); ci != "" { // skip if test on CI
		return
	}

	client := http.DefaultClient

	t.Logf("testing connection to %s", url)
	resp, err := doRequest(client, url)
	if err != nil {
		t.Errorf("Get %s failed: %v", url, err)
	}

	if resp.StatusCode == 403 {
		t.Log("Default client is detected, switching to client with utls transport")
		headers := util.BrowserHeaders()
		client.Transport = utlsx.NewUTLSHTTPRoundTripperWithProxy(
			utls.HelloChrome_Auto, new(utls.Config),
			http.DefaultTransport, nil, &headers,
		)
		resp, err = doRequest(client, url)
		if err != nil {
			t.Errorf("Get %s failed: %v", url, err)
		}
		if resp.StatusCode == 403 {
			t.Fail()
		} else {
			t.Log("Client with utls transport passed Cloudflare detection")
		}
	} else {
		t.Log("Default client passed Cloudflare detection")
	}
}

func doRequest(client *http.Client, url string) (*http.Response, error) {
	resp, err := client.Get(url)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()
	return resp, nil
}
