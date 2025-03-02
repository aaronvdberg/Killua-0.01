# How does Tor use Application Proxy (SOCKS)?

## Overview

The term **"Onion Proxy"** refers to the entire Tor client process, which facilitates anonymous communication through the Tor network. The **SOCKS interface** is a method for a client application to connect to the Onion Proxy. The SOCKS server is provided by the Tor process itself, which attaches the connection to an existing or newly created Tor circuit upon receiving a request.

## Why SOCKS?

SOCKS is used because most applications are designed to communicate over the SOCKS protocol, rather than the Tor protocol directly. While applications could theoretically communicate using the Tor protocol, it's generally safer and easier to use the existing SOCKS interface. SOCKS is a simple, flexible protocol that makes it easier for applications to work with Tor.

Additionally, both **SOCKS4a** and **SOCKS5** support connecting directly to a hostname, reducing the likelihood of DNS leaks, which is a significant benefit when using Tor for privacy.

## How Does Tor Work with SOCKS?

The Onion Proxy is responsible for all Tor-specific operations, including key exchanges, circuit creation, consensus fetching, and descriptor fetching. It acts as an intermediary between the Tor network and the client application. When a client application sends a request to connect to a resource via Tor, the request is routed through a Tor circuit by the Onion Proxy.

The **Tor process** ensures that the request is anonymized before it leaves the Tor network, providing privacy and security for the user.

### Transparent Proxying

Tor also provides an option known as **TransPort** for **Transparent Proxying**. This is another method for proxying traffic into the Tor network, but it is considered a different type of application proxy. Transparent proxying intercepts traffic at the network level and routes it through the Tor network, without the need for the application to explicitly configure a proxy.

## Use Cases for SOCKS with Tor

SOCKS can be used in various scenarios to anonymize internet traffic. Here are a few typical examples:

- **Web Browsing**: Many users configure their web browsers to use Tor via SOCKS proxies to browse the web anonymously.
- **Applications**: Any application that supports SOCKS can be configured to route traffic through Tor, such as instant messaging, email clients, or even custom software.
- **Data Scraping**: Tools like the script below can be used to scrape data via search engines or websites anonymously by routing the requests through Tor's SOCKS interface.

---
## Detailed Explanation of Each Argument

### `--proxy`:
- **Description**: Specifies the Tor proxy server to use for routing traffic.
- **Default**: `127.0.0.1:9050`
- **Usage**: If you want to use a proxy other than the default Tor proxy, specify the proxy's address and port here.
- **Example**: `--proxy 127.0.0.1:9050`

### `--output`:
- **Description**: Defines the format of the output file.
- **Default**: `output_$SEARCH_$DATE.txt`
- **Usage**: Specify the name of the file where the results will be written. You can use placeholders like `$SEARCH` and `$DATE` for dynamic filenames.
- **Example**: `--output results.txt`

### `--continuous_write`:
- **Description**: Determines whether to write to the output file progressively.
- **Default**: `False`
- **Usage**: If set to `True`, the script will append results to the file continuously, instead of overwriting it.
- **Example**: `--continuous_write True`

### `search`:
- **Description**: The search term or phrase to query across search engines.
- **Usage**: This is a required argument that defines the search keyword for the script.
- **Example**: `search "python tutorial"`

### `--limit`:
- **Description**: Limits the number of pages to load per search engine.
- **Default**: `0` (no limit)
- **Usage**: Use this option to restrict how many pages the script should load from each engine.
- **Example**: `--limit 5`

### `--engines`:
- **Description**: A list of search engines to query.
- **Usage**: Specify which search engines to use for the queries. If left blank, all supported engines will be used.
- **Example**: `--engines "Google" "Bing"`

### `--exclude`:
- **Description**: A list of search engines to exclude from the queries.
- **Usage**: If you want to exclude certain search engines, use this option.
- **Example**: `--exclude "Yahoo"`

### `--fields`:
- **Description**: Specifies which fields to output to the CSV file.
- **Usage**: Choose which fields should be included in the CSV output. Multiple fields can be specified.
- **Example**: `--fields "Title" "URL" "Snippet"`

### `--field_delimiter`:
- **Description**: Defines the delimiter used for separating fields in the CSV file.
- **Default**: `,`
- **Usage**: Change the delimiter if necessary (for example, use a semicolon `;` for European formats).
- **Example**: `--field_delimiter ";"`

### `--mp_units`:
- **Description**: Specifies the number of processing units (CPU cores) to use for parallel processing.
- **Default**: `DEFAULT_MP_UNITS`
- **Usage**: Set this to control how many CPU cores the script should utilize for multiprocessing.
- **Example**: `--mp_units 4`
