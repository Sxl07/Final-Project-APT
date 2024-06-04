package functions

import (
	"encoding/json"
	"fmt"
	"net"
)

type Response struct {
	Result []string `json:"result"`
}

func OnServer(port string) (net.Conn, error) {

	conn, err := net.Dial("tcp", port)
	if err != nil {
		return nil, fmt.Errorf("error connecting to server")
	}
	return conn, nil
}

func SendData(data []byte, conn net.Conn) error {

	_, err := conn.Write(data)
	if err != nil {
		return fmt.Errorf("error sendind data")
	}

	fmt.Println("Data sent to the server:", string(data))
	return nil
}
func DataResponse(conn net.Conn) (*Response, error) {
	var response Response
	err := json.NewDecoder(conn).Decode(&response)
	if err != nil {
		return nil, fmt.Errorf("error decoding the JSON response: %v", err)
	}
	return &response, nil
}
