# Search Results

## Document: web-0

### Chunk #0
GitHub - anchore/grype: A vulnerability scanner for container images and filesystems
Skip to content
Navigation Menu
Toggle navigation
            Sign in
        Product
GitHub Copilot
        Write better code with AI
Security
        Find and fix vulnerabilities
Actions
        Automate any workflow
Codespaces
        Instant dev environments
Issues
        Plan and track work
Code Review
        Manage code changes
Discussions
        Collaborate outside of code
Code Search
        Find more, search less
Explore
      All features
      Documentation
      GitHub Skills
      Blog
        Solutions
By company size
      Enterprises
      Small and medium teams
      Startups
      Nonprofits
By use case
      DevSecOps
      DevOps
      CI/CD
      View all use cases
By industry
      Healthcare
      Financial services
      Manufacturing
      Government
      View all industries
              View all solutions
        Resources
Topics
      AI
      DevOps
      Security
      Software Development
      View all
Explore
      Learning Pathways
      White papers, Ebooks, Webinars
      Customer Stories
      Partners
      Executive Insights
        Open Source
GitHub Sponsors
        Fund open source developers
The ReadME Project
        GitHub community articles
Repositories
      Topics
      Trending
      Collections
        Enterprise
Enterprise platform
        AI-powered developer platform
Available add-ons
Advanced Security
        Enterprise-grade security features
GitHub Copilot
        Enterprise-grade AI features
Premium Support
        Enterprise-grade 24/7 support
Pricing
Search or jump to... Search code, repositories, users, issues, pull requests...

### Chunk #1
Search
Clear
Search syntax tips
        Provide feedback
We read every piece of feedback, and take your input very seriously. Include my email address so I can be contacted
    Cancel
    Submit feedback
        Saved searches
Use saved searches to filter your results more quickly
Name
Query
            To see all available qualifiers, see our
documentation
.     Cancel
    Create saved search
                Sign in
                Sign up
Reseting focus
You signed in with another tab or window.
Reload
 to refresh your session. You signed out in another tab or window.
Reload
 to refresh your session. You switched accounts on another tab or window.
Reload
 to refresh your session.

### Chunk #2
Dismiss alert
        anchore
/
grype
Public
Notifications
You must be signed in to change notification settings
Fork
601
          Star
9.4k
        A vulnerability scanner for container images and filesystems
License
     Apache-2.0 license
9.4k
          stars
601
          forks
Branches
Tags
Activity
          Star
Notifications
You must be signed in to change notification settings
Code
Issues
280
Pull requests
19
Actions
Projects
0
Security
Insights
Additional navigation options
          Code
          Issues
          Pull requests
          Actions
          Projects
          Security
          Insights
anchore/grype
main
Branches
Tags
Go to file
Code
Folders and files
Name
Name
Last commit message
Last commit date
Latest commit
History
1,616 Commits
.github
.github
cmd/
grype
cmd/
grype
grype
grype
internal
internal
schema
schema
templates
templates
test
test
.binny.yaml
.binny.yaml
.bouncer.yaml
.bouncer.yaml
.chronicle.yaml
.chronicle.yaml
.gitignore
.gitignore
.gitmodules
.gitmodules
.golangci.yaml
.golangci.yaml
.goreleaser.yaml
.goreleaser.yaml
CODE_OF_CONDUCT.md
CODE_OF_CONDUCT.md
CONTRIBUTING.md
CONTRIBUTING.md
DEVELOPING.md
DEVELOPING.md
Dockerfile
Dockerfile
Dockerfile.debug
Dockerfile.debug
LICENSE
LICENSE
Makefile
Makefile
README.md
README.md
RELEASE.md
RELEASE.md
SECURITY.md
SECURITY.md
Taskfile.yaml
Taskfile.yaml
artifacthub-repo.yml
artifacthub-repo.yml
go.mod
go.mod
go.sum
go.sum
install.sh
install.sh
View all files
Repository files navigation
README
Code of conduct
Apache-2.0 license
Security
A vulnerability scanner for container images and filesystems.

### Chunk #3
Easily
install the binary
 to try it out. Works with
Syft
, the powerful SBOM (software bill of materials) tool for container images and filesystems. Join our community meetings! Calendar:
https://calendar.google.com/calendar/u/0/r?cid=Y182OTM4dGt0MjRtajI0NnNzOThiaGtnM29qNEBncm91cC5jYWxlbmRhci5nb29nbGUuY29t
Agenda:
https://docs.google.com/document/d/1ZtSAa6fj2a6KRWviTn3WoJm09edvrNUp4Iz_dOjjyY8/edit?usp=sharing
 (join
this group
 for write access)
All are welcome! For commercial support options with Syft or Grype, please
contact Anchore
Features
Scan the contents of a container image or filesystem to find known vulnerabilities. Find vulnerabilities for major operating system packages:
Alpine
Amazon Linux
BusyBox
CentOS
CBL-Mariner
Debian
Distroless
Oracle Linux
Red Hat (RHEL)
Ubuntu
Wolfi
Find vulnerabilities for language-specific packages:
Ruby (Gems)
Java (JAR, WAR, EAR, JPI, HPI)
JavaScript (NPM, Yarn)
Python (Egg, Wheel, Poetry, requirements.txt/setup.py files)
Dotnet (deps.json)
Golang (go.mod)
PHP (Composer)
Rust (Cargo)
Supports Docker, OCI and
Singularity
 image formats. OpenVEX
 support for filtering and augmenting scanning results. If you encounter an issue, please
let us know using the issue tracker
.

### Chunk #4
Installation
Recommended
curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh
|
 sh -s -- -b /usr/local/bin
Install script options:
-b
: Specify a custom installation directory (defaults to
./bin
)
-d
: More verbose logging levels (
-d
 for debug,
-dd
 for trace)
-v
: Verify the signature of the downloaded artifact before installation (requires
cosign
 to be installed)
Chocolatey
The chocolatey distribution of grype is community-maintained and not distributed by the anchore team. choco install grype -y
Homebrew
brew tap anchore/grype
brew install grype
MacPorts
On macOS, Grype can additionally be installed from the
community-maintained port
 via MacPorts:
sudo port install grype
Note
: Currently, Grype is built only for macOS and Linux. From source
See
DEVELOPING.md
 for instructions to build and run from source. GitHub Actions
If you're using GitHub Actions, you can use our
Grype-based action
 to run vulnerability scans on your code or container images during your CI workflows. Verifying the artifacts
Checksums are applied to all artifacts, and the resulting checksum file is signed using cosign.

### Chunk #5
You need the following tool to verify signature:
Cosign
Verification steps are as follow:
Download the files you want, and the checksums.txt, checksums.txt.pem and checksums.txt.sig files from the
releases
 page:
Verify the signature:
cosign verify-blob
<
path to checksum.txt
>
 \
--certificate
<
path to checksums.txt.pem
>
 \
--signature
<
path to checksums.txt.sig
>
 \
--certificate-identity-regexp
'
https://github\.com/anchore/grype/\.github/workflows/.+
'
 \
--certificate-oidc-issuer
"
https://token.actions.githubusercontent.com
"
Once the signature is confirmed as valid, you can proceed to validate that the SHA256 sums align with the downloaded artifact:
sha256sum --ignore-missing -c checksums.txt
Getting started
Install the binary
, and make sure that
grype
 is available in your path. To scan for vulnerabilities in an image:
grype <image>
The above command scans for vulnerabilities visible in the container (i.e., the squashed representation of the image).

### Chunk #6
To include software from all image layers in the vulnerability scan, regardless of its presence in the final image, provide
--scope all-layers
:
grype <image> --scope all-layers
To run grype from a Docker container so it can scan a running container, use the following command:
docker run --rm \
--volume /var/run/docker.sock:/var/run/docker.sock \
--name Grype anchore/grype:latest \
$(ImageName):$(ImageTag)
Supported sources
Grype can scan a variety of sources beyond those found in Docker.

### Chunk #7
# scan a container image archive (from the result of `docker image save ...`, `podman save ...`, or `skopeo copy` commands)
grype path/to/image.tar
# scan a Singularity Image Format (SIF) container
grype path/to/image.sif
# scan a directory
grype dir:path/to/dir
Sources can be explicitly provided with a scheme:
podman:yourrepo/yourimage:tag          use images from the Podman daemon
docker:yourrepo/yourimage:tag          use images from the Docker daemon
docker-archive:path/to/yourimage.tar   use a tarball from disk for archives created from "docker save"
oci-archive:path/to/yourimage.tar      use a tarball from disk for OCI archives (from Skopeo or otherwise)
oci-dir:path/to/yourimage              read directly from a path on disk for OCI layout directories (from Skopeo or otherwise)
singularity:path/to/yourimage.sif      read directly from a Singularity Image Format (SIF) container on disk
dir:path/to/yourproject                read directly from a path on disk (any directory)
file:path/to/yourfile                  read directly from a file on disk
sbom:path/to/syft.json                 read Syft JSON from path on disk
registry:yourrepo/yourimage:tag        pull image directly from a registry (no container runtime required)
If an image source is not provided and cannot be detected from the given reference it is assumed the image should be pulled from the Docker daemon.

### Chunk #8
If docker is not present, then the Podman daemon is attempted next, followed by reaching out directly to the image registry last. This default behavior can be overridden with the
default-image-pull-source
 configuration option (See
Configuration
 for more details). Use SBOMs for even faster vulnerability scanning in Grype:
# Then scan for new vulnerabilities as frequently as needed
grype sbom:./sbom.json
# (You can also pipe the SBOM into Grype)
cat ./sbom.json | grype
Grype supports input of
Syft
,
SPDX
, and
CycloneDX
SBOM formats. If Syft has generated any of these file types, they should have the appropriate information to work properly with Grype. It is also possible to use SBOMs generated by other tools with varying degrees of success. Two things that make Grype matching
more successful are the inclusion of CPE and Linux distribution information. If an SBOM does not include any CPE information, it
is possible to generate these based on package information using the
--add-cpes-if-none
 flag. To specify a distribution,
use the
--distro <distro>:<version>
 flag.

### Chunk #9
A full example is:
grype --add-cpes-if-none --distro alpine:3.10 sbom:some-alpine-3.10.spdx.json
Supported versions
Any version of Grype before v0.51.0 (Oct 2022) is not supported. Unsupported releases will not receive any software updates or
vulnerability database updates. You can still build vulnerability databases for unsupported Grype releases by using previous
releases of
vunnel
 to gather the upstream data and
grype-db
to build databases for unsupported schemas. Working with attestations
Grype supports scanning SBOMs as input via stdin. Users can use
cosign
 to verify attestations
with an SBOM as its content to scan an image for vulnerabilities:
COSIGN_EXPERIMENTAL=1 cosign verify-attestation caphill4/java-spdx-tools:latest \
| jq -r .payload \
| base64 --decode \
| jq -r .predicate.Data \
| grype
Vulnerability Summary
Basic Grype Vulnerability Data Shape
 {
"vulnerability"
: {
...   },
"relatedVulnerabilities"
: [
...   ],
"matchDetails"
: [
...   ],
"artifact"
: {
...   }
}
Vulnerability
: All information on the specific vulnerability that was directly matched on (e.g. ID, severity, CVSS score, fix information, links for more information)
RelatedVulnerabilities
: Information pertaining to vulnerabilities found to be related to the main reported vulnerability. Maybe the vulnerability we matched on was a GitHub Security Advisory, which has an upstream CVE (in the authoritative national vulnerability database).

### Chunk #10
In these cases we list the upstream vulnerabilities here. MatchDetails
: This section tries to explain what we searched for while looking for a match and exactly what details on the package and vulnerability that lead to a match. Artifact
: This is a subset of the information that we know about the package (when compared to the
Syft
 json output, we summarize the metadata section). This has information about where within the container image or directory we found the package, what kind of package it is, licensing info, pURLs, CPEs, etc. Excluding file paths
Grype can exclude files and paths from being scanned within a source by using glob expressions
with one or more
--exclude
 parameters:
grype <source> --exclude './out/**/*.json' --exclude /etc
Note:
 in the case of
image scanning
, since the entire filesystem is scanned it is
possible to use absolute paths like
/etc
 or
/usr/**/*.txt
 whereas
directory scans
exclude files
relative to the specified directory
. For example: scanning
/usr/foo
 with
--exclude ./package.json
 would exclude
/usr/foo/package.json
 and
--exclude '**/package.json'
would exclude all
package.json
 files under
/usr/foo
.

### Chunk #11
For
directory scans
,
it is required to begin path expressions with
./
,
*/
, or
**/
, all of which
will be resolved
relative to the specified scan directory
. Keep in mind, your shell
may attempt to expand wildcards, so put those parameters in single quotes, like:
'**/*.json'
. External Sources
Grype can be configured to incorporate external data sources for added fidelity in vulnerability matching. This
feature is currently disabled by default. To enable this feature add the following to the grype config:
external-sources
:
enable
:
true
maven
:
search-upstream-by-sha1
:
true
base-url
:
https://search.maven.org/solrsearch/select
rate-limit
:
300ms
#
 Time between Maven API requests
You can also configure the base-url if you're using another registry as your maven endpoint. The rate at which Maven API requests are made can be configured to match your environment's requirements. The default is 300ms between requests. Output formats
The output format for Grype is configurable as well:
grype <image> -o <format>
Where the formats available are:
table
: A columnar summary (default). cyclonedx
: An XML report conforming to the
CycloneDX 1.6 specification
. cyclonedx-json
: A JSON report conforming to the
CycloneDX 1.6 specification
.

### Chunk #12
json
: Use this to get as much information out of Grype as possible! sarif
: Use this option to get a
SARIF
 report (Static Analysis Results Interchange Format)
template
: Lets the user specify the output format. See
"Using templates"
 below. Using templates
Grype lets you define custom output formats, using
Go templates
. Here's how it works:
Define your format as a Go template, and save this template as a file. Set the output format to "template" (
-o template
). Specify the path to the template file (
-t ./path/to/custom.template
). Grype's template processing uses the same data models as the
json
 output format — so if you're wondering what data is available as you author a template, you can use the output from
grype <image> -o json
 as a reference. Please note:
 Templates can access information about the system they are running on, such as environment variables. You should never run untrusted templates. There are several example templates in the
templates
 directory in the Grype source which can serve as a starting point for a custom output format.

### Chunk #13
For example,
csv.tmpl
 produces a vulnerability report in CSV (comma separated value) format:
"Package","Version Installed","Vulnerability ID","Severity"
"coreutils","8.30-3ubuntu2","CVE-2016-2781","Low"
"libc-bin","2.31-0ubuntu9","CVE-2016-10228","Negligible"
"libc-bin","2.31-0ubuntu9","CVE-2020-6096","Low"
... You can also find the template for the default "table" output format in the same place. Grype also includes a vast array of utility templating functions from
sprig
 apart from the default golang
text/template
 to allow users to customize the output from Grype. Gating on severity of vulnerabilities
You can have Grype exit with an error if any vulnerabilities are reported at or above the specified severity level. This comes in handy when using Grype within a script or CI pipeline. To do this, use the
--fail-on <severity>
 CLI flag.

### Chunk #14
For example, here's how you could trigger a CI pipeline failure if any vulnerabilities are found in the
ubuntu:latest
 image with a severity of "medium" or higher:
grype ubuntu:latest --fail-on medium
Specifying matches to ignore
If you're seeing Grype report
false positives
 or any other vulnerability matches that you just don't want to see, you can tell Grype to
ignore
 matches by specifying one or more
"ignore rules"
 in your Grype configuration file (e.g.
~/.grype.yaml
). This causes Grype not to report any vulnerability matches that meet the criteria specified by any of your ignore rules.

### Chunk #15
Each rule can specify any combination of the following criteria:
vulnerability ID (e.g.
"CVE-2008-4318"
)
namespace (e.g.
"nvd"
)
fix state (allowed values:
"fixed"
,
"not-fixed"
,
"wont-fix"
, or
"unknown"
)
package name (e.g.
"libcurl"
)
package version (e.g.
"1.5.1"
)
package language (e.g.
"python"
; these values are defined
here
)
package type (e.g.
"npm"
; these values are defined
here
)
package location (e.g.
"/usr/local/lib/node_modules/**"
; supports glob patterns)
Here's an example
~/.grype.yaml
 that demonstrates the expected format for ignore rules:
ignore
:
#
 This is the full set of supported rule fields:
  -
vulnerability
:
CVE-2008-4318
fix-state
:
unknown
#
 VEX fields apply when Grype reads vex data:
vex-status
:
not_affected
vex-justification
:
vulnerable_code_not_present
package
:
name
:
libcurl
version
:
1.5.1
type
:
npm
location
:
"
/usr/local/lib/node_modules/**
"
#
 We can make rules to match just by vulnerability ID:
  -
vulnerability
:
CVE-2014-54321
#
 ...or just by a single package field:
  -
package
:
type
:
gem
Vulnerability matches will be ignored if
any
 rules apply to the match. A rule is considered to apply to a given vulnerability match only if
all
 fields specified in the rule apply to the vulnerability match.

### Chunk #16
When you run Grype while specifying ignore rules, the following happens to the vulnerability matches that are "ignored":
Ignored matches are
completely hidden
 from Grype's output, except for when using the
json
 or
template
 output formats; however, in these two formats, the ignored matches are
removed
 from the existing
matches
 array field, and they are placed in a new
ignoredMatches
 array field. Each listed ignored match also has an additional field,
appliedIgnoreRules
, which is an array of any rules that caused Grype to ignore this vulnerability match. Ignored matches
do not
 factor into Grype's exit status decision when using
--fail-on <severity>
. For instance, if a user specifies
--fail-on critical
, and all of the vulnerability matches found with a "critical" severity have been
ignored
, Grype will exit zero. Note:
 Please continue to
report
 any false positives you see! Even if you can reliably filter out false positives using ignore rules, it's very helpful to the Grype community if we have as much knowledge about Grype's false positives as possible. This helps us continuously improve Grype!

### Chunk #17
Showing only "fixed" vulnerabilities
If you only want Grype to report vulnerabilities
that have a confirmed fix
, you can use the
--only-fixed
 flag. (This automatically adds
ignore rules
 into Grype's configuration, such that vulnerabilities that aren't fixed will be ignored.)
For example, here's a scan of Alpine 3.10:
NAME          INSTALLED  FIXED-IN   VULNERABILITY   SEVERITY
apk-tools     2.10.6-r0  2.10.7-r0  CVE-2021-36159  Critical
libcrypto1.1  1.1.1k-r0             CVE-2021-3711   Critical
libcrypto1.1  1.1.1k-r0             CVE-2021-3712   High
libssl1.1     1.1.1k-r0             CVE-2021-3712   High
libssl1.1     1.1.1k-r0             CVE-2021-3711   Critical
...and here's the same scan, but adding the flag
--only-fixed
:
NAME       INSTALLED  FIXED-IN   VULNERABILITY   SEVERITY
apk-tools  2.10.6-r0  2.10.7-r0  CVE-2021-36159  Critical
If you want Grype to only report vulnerabilities
that do not have a confirmed fix
, you can use the
--only-notfixed
 flag. Alternatively, you can use the
--ignore-states
 flag to filter results for vulnerabilities with specific states such as
wont-fix
 (see
--help
 for a list of valid fix states).

### Chunk #18
These flags automatically add
ignore rules
 into Grype's configuration, such that vulnerabilities which are fixed, or will not be fixed, will be ignored. VEX Support
Grype can use VEX (Vulnerability Exploitability Exchange) data to filter false
positives or provide additional context, augmenting matches. When scanning a
container image, you can use the
--vex
 flag to point to one or more
OpenVEX
 documents. VEX statements relate a product (a container image), a vulnerability, and a VEX
status to express an assertion of the vulnerability's impact. There are four
VEX statuses
:
not_affected
,
affected
,
fixed
 and
under_investigation
. Here is an example of a simple OpenVEX document. (tip: use
vexctl
 to generate your own documents).

### Chunk #19
{
"@context"
:
"
https://openvex.dev/ns/v0.2.0
"
,
"@id"
:
"
https://openvex.dev/docs/public/vex-d4e9020b6d0d26f131d535e055902dd6ccf3e2088bce3079a8cd3588a4b14c78
"
,
"author"
:
"
A Grype User <jdoe@example.com>
"
,
"timestamp"
:
"
2023-07-17T18:28:47.696004345-06:00
"
,
"version"
:
1
,
"statements"
: [
    {
"vulnerability"
: {
"name"
:
"
CVE-2023-1255
"
      },
"products"
: [
        {
"@id"
:
"
pkg:oci/alpine@sha256%3A124c7d2707904eea7431fffe91522a01e5a861a624ee31d03372cc1d138a3126
"
,
"subcomponents"
: [
            {
"@id"
:
"
pkg:apk/alpine/libssl3@3.0.8-r3
"
 },
            {
"@id"
:
"
pkg:apk/alpine/libcrypto3@3.0.8-r3
"
 }
          ]
        }
      ],
"status"
:
"
fixed
"
    }
  ]
}
By default, Grype will use any statements in specified VEX documents with a
status of
not_affected
 or
fixed
 to move matches to the ignore set. Any matches ignored as a result of VEX statements are flagged when using
--show-suppressed
:
libcrypto3  3.0.8-r3   3.0.8-r4   apk   CVE-2023-1255  Medium (suppressed by VEX)
Statements with an
affected
 or
under_investigation
 status will only be
considered to augment the result set when specifically requested using the
GRYPE_VEX_ADD
 environment variable or in a configuration file. VEX Ignore Rules
Ignore rules can be written to control how Grype honors VEX statements.

### Chunk #20
For
example, to configure Grype to only act on VEX statements when the justification is
vulnerable_code_not_present
, you can write a rule like this:
---
ignore
:
  -
vex-status
:
not_affected
vex-justification
:
vulnerable_code_not_present
See the
list of justifications
 for details. You can mix
vex-status
 and
vex-justification
with other ignore rule parameters. Grype's database
When Grype performs a scan for vulnerabilities, it does so using a vulnerability database that's stored on your local filesystem, which is constructed by pulling data from a variety of publicly available vulnerability data sources.

### Chunk #21
These sources include:
Alpine Linux SecDB:
https://secdb.alpinelinux.org/
Amazon Linux ALAS:
https://alas.aws.amazon.com/AL2/alas.rss
Chainguard SecDB:
https://packages.cgr.dev/chainguard/security.json
Debian Linux CVE Tracker:
https://security-tracker.debian.org/tracker/data/json
GitHub Security Advisories (GHSAs):
https://github.com/advisories
National Vulnerability Database (NVD):
https://nvd.nist.gov/vuln/data-feeds
Oracle Linux OVAL:
https://linux.oracle.com/security/oval/
RedHat Linux Security Data:
https://access.redhat.com/hydra/rest/securitydata/
RedHat RHSAs:
https://www.redhat.com/security/data/oval/
SUSE Linux OVAL:
https://ftp.suse.com/pub/projects/security/oval/
Ubuntu Linux Security:
https://people.canonical.com/~ubuntu-security/
Wolfi SecDB:
https://packages.wolfi.dev/os/security.json
By default, Grype automatically manages this database for you. Grype checks for new updates to the vulnerability database to make sure that every scan uses up-to-date vulnerability information. This behavior is configurable. For more information, see the
Managing Grype's database
 section. How database updates work
Grype's vulnerability database is a SQLite file, named
vulnerability.db
. Updates to the database are atomic: the entire database is replaced and then treated as "readonly" by Grype.

### Chunk #22
Grype's first step in a database update is discovering databases that are available for retrieval. Grype does this by requesting a "listing file" from a public endpoint:
https://toolbox-data.anchore.io/grype/databases/listing.json
The listing file contains entries for every database that's available for download. Here's an example of an entry in the listing file:
{
"built"
:
"
2021-10-21T08:13:41Z
"
,
"version"
:
3
,
"url"
:
"
https://toolbox-data.anchore.io/grype/databases/vulnerability-db_v3_2021-10-21T08:13:41Z.tar.gz
"
,
"checksum"
:
"
sha256:8c99fb4e516f10b304f026267c2a73a474e2df878a59bf688cfb0f094bfe7a91
"
}
With this information, Grype can select the correct database (the most recently built database with the current schema version), download the database, and verify the database's integrity using the listed
checksum
 value. Managing Grype's database
Note:
 During normal usage,
there is no need for users to manage Grype's database!  Grype manages its database behind the scenes. However, for users that need more control, Grype provides options to manage the database more explicitly. Local database cache directory
By default, the database is cached on the local filesystem in the directory
$XDG_CACHE_HOME/grype/db/<SCHEMA-VERSION>/
. For example, on macOS, the database would be stored in
~/Library/Caches/grype/db/3/
.

### Chunk #23
(For more information on XDG paths, refer to the
XDG Base Directory Specification
.)
You can set the cache directory path using the environment variable
GRYPE_DB_CACHE_DIR
. If setting that variable alone does not work, then the
TMPDIR
 environment variable might also need to be set. Data staleness
Grype needs up-to-date vulnerability information to provide accurate matches. By default, it will fail execution if the local database was not built in the last 5 days. The data staleness check is configurable via the environment variable
GRYPE_DB_MAX_ALLOWED_BUILT_AGE
 and
GRYPE_DB_VALIDATE_AGE
 or the field
max-allowed-built-age
 and
validate-age
, under
db
. It uses
golang's time duration syntax
. Set
GRYPE_DB_VALIDATE_AGE
 or
validate-age
 to
false
 to disable staleness check. Offline and air-gapped environments
By default, Grype checks for a new database on every run, by making a network call over the Internet. You can tell Grype not to perform this check by setting the environment variable
GRYPE_DB_AUTO_UPDATE
 to
false
. As long as you place Grype's
vulnerability.db
 and
metadata.json
 files in the cache directory for the expected schema version, Grype has no need to access the network.

### Chunk #24
Additionally, you can get a listing of the database archives available for download from the
grype db list
 command in an online environment, download the database archive, transfer it to your offline environment, and use
grype db import <db-archive-path>
 to use the given database in an offline capacity. If you would like to distribute your own Grype databases internally without needing to use
db import
 manually you can leverage Grype's DB update mechanism. To do this you can craft your own
listing.json
 file similar to the one found publically (see
grype db list -o raw
 for an example of our public
listing.json
 file) and change the download URL to point to an internal endpoint (e.g. a private S3 bucket, an internal file server, etc). Any internal installation of Grype can receive database updates automatically by configuring the
db.update-url
 (same as the
GRYPE_DB_UPDATE_URL
 environment variable) to point to the hosted
listing.json
 file you've crafted. CLI commands for database management
Grype provides database-specific CLI commands for users that want to control the database from the command line.

### Chunk #25
Here are some of the useful commands provided:
grype db status
 — report the current status of Grype's database (such as its location, build date, and checksum)
grype db check
 — see if updates are available for the database
grype db update
 — ensure the latest database has been downloaded to the cache directory (Grype performs this operation at the beginning of every scan by default)
grype db list
 — download the listing file configured at
db.update-url
 and show databases that are available for download
grype db import
 — provide grype with a database archive to explicitly use (useful for offline DB updates)
grype db providers
 - provides a detailed list of database providers
Find complete information on Grype's database commands by running
grype db --help
. Shell completion
Grype supplies shell completion through its CLI implementation (
cobra
). Generate the completion code for your shell by running one of the following commands:
grype completion <bash|zsh|fish>
go run ./cmd/grype completion <bash|zsh|fish>
This will output a shell script to STDOUT, which can then be used as a completion script for Grype.

### Chunk #26
Running one of the above commands with the
-h
 or
--help
 flags will provide instructions on how to do that for your chosen shell. Private Registry Authentication
Local Docker Credentials
When a container runtime is not present, grype can still utilize credentials configured in common credential sources (such as
~/.docker/config.json
). It will pull images from private registries using these credentials. The config file is where your credentials are stored when authenticating with private registries via some command like
docker login
. For more information see the
go-containerregistry
documentation
. An example
config.json
 looks something like this:
// config.json
{
  "auths": {
    "registry.example.com": {
      "username": "AzureDiamond",
      "password": "hunter2"
    }
  }
}
You can run the following command as an example. It details the mount/environment configuration a container needs to access a private registry:
docker run -v ./config.json:/config/config.json -e "DOCKER_CONFIG=/config" anchore/grype:latest <private_image>
Docker Credentials in Kubernetes
The below section shows a simple workflow on how to mount this config file as a secret into a container on kubernetes. Create a secret. The value of
config.json
 is important. It refers to the specification detailed
here
.

### Chunk #27
Below this section is the
secret.yaml
 file that the pod configuration will consume as a volume. The key
config.json
 is important. It will end up being the name of the file when mounted into the pod.     apiVersion: v1
    kind: Secret
    metadata:
      name: registry-config
      namespace: grype
    data:
      config.json: <base64 encoded config.json>
    ```
    `kubectl apply -f secret.yaml`
Create your pod running grype. The env
DOCKER_CONFIG
 is important because it advertises where to look for the credential file. In the below example, setting
DOCKER_CONFIG=/config
 informs grype that credentials can be found at
/config/config.json
. This is why we used
config.json
 as the key for our secret. When mounted into containers the secrets' key is used as the filename. The
volumeMounts
 section mounts our secret to
/config
. The
volumes
 section names our volume and leverages the secret we created in step one.     apiVersion: v1
    kind: Pod
    spec:
      containers:
        - image: anchore/grype:latest
          name: grype-private-registry-demo
          env:
            - name: DOCKER_CONFIG
              value: /config
          volumeMounts:
          - mountPath: /config
            name: registry-config
            readOnly: true
          args:
            - <private_image>
      volumes:
      - name: registry-config
        secret:
          secretName: registry-config
    ```
    `kubectl apply -f pod.yaml`
The user can now run
kubectl logs grype-private-registry-demo
.

### Chunk #28
The logs should show the grype analysis for the
<private_image>
 provided in the pod configuration. Using the above information, users should be able to configure private registry access without having to do so in the
grype
 or
syft
 configuration files. They will also not be dependent on a docker daemon, (or some other runtime software) for registry configuration and access. Configuration
Default configuration search paths (see all with
grype config locations
):
.grype.yaml
.grype/config.yaml
~/.grype.yaml
<XDG_CONFIG_HOME>/grype/config.yaml
Use
grype config
 to print a sample config file to stdout. Use
grype config --load
 to print the current config after loading all values to stdout.

### Chunk #29
You can specify files directly using the
--config
 /
-c
 flags (or environment variable
GRYPE_CONFIG
) to provide your own configuration files/paths:
#
 Using the flag
grype
<
image
>
 -c /path/to/config.yaml
#
 Or using the environment variable
GRYPE_CONFIG=/path/to/config.yaml grype
<
image
>
Configuration options (example values are the default):
#
 enable/disable checking for application updates on startup
#
 same as GRYPE_CHECK_FOR_APP_UPDATE env var
check-for-app-update
:
true
#
 allows users to specify which image source should be used to generate the sbom
#
 valid values are: registry, docker, podman
#
 same as GRYPE_DEFAULT_IMAGE_PULL_SOURCE env var
default-image-pull-source
:
"
"
#
 same as --name; set the name of the target being analyzed
name
:
"
"
#
 upon scanning, if a severity is found at or above the given severity then the return code will be 1
#
 default is unset which will skip this validation (options: negligible, low, medium, high, critical)
#
 same as --fail-on ; GRYPE_FAIL_ON_SEVERITY env var
fail-on-severity
:
"
"
#
 the output format of the vulnerability report (options: table, template, json, cyclonedx)
#
 when using template as the output type, you must also provide a value for 'output-template-file'
#
 same as -o ; GRYPE_OUTPUT env var
output
:
"
table
"
#
 if using template output, you must provide a path to a Go template file
#
 see https://github.com/anchore/grype#using-templates for more information on template output
#
 the default path to the template file is the current working directory
#
 output-template-file: .grype/html.tmpl
#
 write output report to a file (default is to write to stdout)
#
 same as --file; GRYPE_FILE env var
file
:
"
"
#
 a list of globs to exclude from scanning, for example:
#
 exclude:
#
   - '/etc/**'
#
   - './out/**/*.json'
#
 same as --exclude ; GRYPE_EXCLUDE env var
exclude
:
[]
#
 include matches on kernel-headers packages that are matched against upstream kernel package
#
 if 'false' any such matches are marked as ignored
match-upstream-kernel-headers
:
false
#
 os and/or architecture to use when referencing container images (e.g. "windows/armv6" or "arm64")
#
 same as --platform; GRYPE_PLATFORM env var
platform
:
"
"
#
 If using SBOM input, automatically generate CPEs when packages have none
add-cpes-if-none
:
false
#
 Explicitly specify a linux distribution to use as <distro>:<version> like alpine:3.10
distro
:
external-sources
:
enable
:
false
maven
:
search-upstream-by-sha1
:
true
base-url
:
https://search.maven.org/solrsearch/select
rate-limit
:
300ms
db
:
#
 check for database updates on execution
#
 same as GRYPE_DB_AUTO_UPDATE env var
auto-update
:
true
#
 location to write the vulnerability database cache; defaults to $XDG_CACHE_HOME/grype/db
#
 same as GRYPE_DB_CACHE_DIR env var
cache-dir
:
"
"
#
 URL of the vulnerability database
#
 same as GRYPE_DB_UPDATE_URL env var
update-url
:
"
https://toolbox-data.anchore.io/grype/databases/listing.json
"
#
 it ensures db build is no older than the max-allowed-built-age
#
 set to false to disable check
validate-age
:
true
#
 Max allowed age for vulnerability database,
#
 age being the time since it was built
#
 Default max age is 120h (or five days)
max-allowed-built-age
:
"
120h
"
#
 Timeout for downloading GRYPE_DB_UPDATE_URL to see if the database needs to be downloaded
#
 This file is ~156KiB as of 2024-04-17 so the download should be quick; adjust as needed
update-available-timeout
:
"
30s
"
#
 Timeout for downloading actual vulnerability DB
#
 The DB is ~156MB as of 2024-04-17 so slower connections may exceed the default timeout; adjust as needed
update-download-timeout
:
"
120s
"
search
:
#
 the search space to look for packages (options: all-layers, squashed)
#
 same as -s ; GRYPE_SEARCH_SCOPE env var
scope
:
"
squashed
"
#
 search within archives that do contain a file index to search against (zip)
#
 note: for now this only applies to the java package cataloger
#
 same as GRYPE_PACKAGE_SEARCH_INDEXED_ARCHIVES env var
indexed-archives
:
true
#
 search within archives that do not contain a file index to search against (tar, tar.gz, tar.bz2, etc)
#
 note: enabling this may result in a performance impact since all discovered compressed tars will be decompressed
#
 note: for now this only applies to the java package cataloger
#
 same as GRYPE_PACKAGE_SEARCH_UNINDEXED_ARCHIVES env var
unindexed-archives
:
false
#
 options when pulling directly from a registry via the "registry:" scheme
registry
:
#
 skip TLS verification when communicating with the registry
#
 same as GRYPE_REGISTRY_INSECURE_SKIP_TLS_VERIFY env var
insecure-skip-tls-verify
:
false
#
 use http instead of https when connecting to the registry
#
 same as GRYPE_REGISTRY_INSECURE_USE_HTTP env var
insecure-use-http
:
false
#
 filepath to a CA certificate (or directory containing *.crt, *.cert, *.pem) used to generate the client certificate
#
 GRYPE_REGISTRY_CA_CERT env var
ca-cert
:
"
"
#
 credentials for specific registries
auth
:
#
 the URL to the registry (e.g. "docker.io", "localhost:5000", etc.)
#
 GRYPE_REGISTRY_AUTH_AUTHORITY env var
    -
authority
:
"
"
#
 GRYPE_REGISTRY_AUTH_USERNAME env var
username
:
"
"
#
 GRYPE_REGISTRY_AUTH_PASSWORD env var
password
:
"
"
#
 note: token and username/password are mutually exclusive
#
 GRYPE_REGISTRY_AUTH_TOKEN env var
token
:
"
"
#
 filepath to the client certificate used for TLS authentication to the registry
#
 GRYPE_REGISTRY_AUTH_TLS_CERT env var
tls-cert
:
"
"
#
 filepath to the client key used for TLS authentication to the registry
#
 GRYPE_REGISTRY_AUTH_TLS_KEY env var
tls-key
:
"
"
#
 - ...

### Chunk #30
# note, more credentials can be provided via config file only (not env vars)
log
:
#
 suppress all output (except for the vulnerability list)
#
 same as -q ; GRYPE_LOG_QUIET env var
quiet
:
false
#
 increase verbosity
#
 same as GRYPE_LOG_VERBOSITY env var
verbosity
:
0
#
 the log level; note: detailed logging suppress the ETUI
#
 same as GRYPE_LOG_LEVEL env var
#
 Uses logrus logging levels: https://github.com/sirupsen/logrus#level-logging
level
:
"
error
"
#
 location to write the log file (default is not to have a log file)
#
 same as GRYPE_LOG_FILE env var
file
:
"
"
match
:
#
 sets the matchers below to use cpes when trying to find
#
 vulnerability matches. The stock matcher is the default
#
 when no primary matcher can be identified. java
:
using-cpes
:
false
python
:
using-cpes
:
false
javascript
:
using-cpes
:
false
ruby
:
using-cpes
:
false
dotnet
:
using-cpes
:
false
golang
:
using-cpes
:
false
#
 even if CPE matching is disabled, make an exception when scanning for "stdlib".

### Chunk #31
always-use-cpe-for-stdlib
:
true
#
 allow main module pseudo versions, which may have only been "guessed at" by Syft, to be used in vulnerability matching
allow-main-module-pseudo-version-comparison
:
false
stock
:
using-cpes
:
true
Future plans
The following areas of potential development are currently being investigated:
Support for allowlist, package mapping
Grype Logo
Grype Logo
 by
Anchore
 is licensed under
CC BY 4.0
About
        A vulnerability scanner for container images and filesystems
Topics
  go
  docker
  golang
  security
  tool
  containers
  static-analysis
  oci
  vulnerability
  vex
  vulnerabilities
  hacktoberfest
  container-image
  cyclonedx
  openvex
Resources
        Readme
License
     Apache-2.0 license
Code of conduct
        Code of conduct
Security policy
        Security policy
Activity
Custom properties
Stars
9.4k
      stars
Watchers
80
      watching
Forks
601
      forks
          Report repository
Releases
153
v0.87.0
          Latest
Jan 22, 2025
+ 152 releases
Packages
0
Contributors
102
+ 88 contributors
Languages
Go
96.0%
Shell
2.7%
Makefile
0.7%
Python
0.3%
Dockerfile
0.2%
Ruby
0.1%
Footer
        © 2025 GitHub, Inc. Footer navigation
Terms
Privacy
Security
Status
Docs
Contact
      Manage cookies
      Do not share my personal information
    You can’t perform that action at this time.

## Document: web-1

### Chunk #0
How to Find Vulnerabilities In Containers and Files With Grype
How-To Geek
Menu
Sign in now
Close
Desktop
Submenu
Windows
Mac
Linux
Chromebook
Microsoft
Programming
Mobile
Submenu
Android
iPhone
Cellular Carriers
Gaming
Streaming
Submenu
Audio/Video
Web
Submenu
Cyber Security
Google
Hobbies
Science
Submenu
Cutting Edge
Space
Automotive
News
Reviews
Buying Guides
Deals
Sign in
Newsletter
Windows
Linux
iPhone
Android
Streaming
Microsoft Excel
Deals
Close
How to Find Vulnerabilities In Containers and Files With Grype
Cybersecurity
By 
James Walker
Published
 Dec 29, 2021
                                            Follow
                                            Followed
                    Like
Link copied to clipboard
Sign in to your
How-To Geek
 account
Quick Links
Installing Grype
Basic Scans
Scanning Filesystems
Filtering Vulnerabilities
Ignoring Vulnerabilities
Using SBOMs
Customizing Grype Output
Vulnerability Database
Summary
Grype is an open-source vulnerability scanner that finds weaknesses within container images and filesystem directories. Grype is
developed by Anchore
 but works as a standalone binary that's easier to get to grips with than the Anchore Engine. Known vulnerabilities make their way into your software via outdated operating system packages, compromised programming language dependencies, and insecure base images. Actively scanning your artifacts keeps you informed of issues before malicious actors find them.

### Chunk #1
Here's how to use Grype to find problems in your code and containers.                         Installing Grype
Grype is distributed as a pre-compiled binary in
deb
,
rpm
, Linux source, and Mac formats. You can grab the latest release
from GitHub
 and install it with your system's package manager or by copying the binary to a location in your path. Alternatively, use the installation script to automate the process:
curl -sSfL https:
//raw.githubusercontent.com/anchore/grype/main/install.sh | sh -s -- -b /usr/local/bin
Check your binary's working by running the
grype
 command. Documentation on the available commands will be displayed.                         Basic Scans
In its simplest form, Grype takes a single argument that specifies the container image or filesystem path to scan. To scan an image, supply a valid registry tag. Grype will use available Docker credentials to pull images from Docker Hub and
private registries
. grype
alpine
:latest
You can also scan
an image archive
 that's been exported from Docker:
grype
saved-image
.tar
Grype will download its vulnerability database the first time it's run. This currently weighs in at about 90MB.

### Chunk #2
Once the database is available, Grype will pull the Docker image, catalogue the software inside it, and parse known vulnerabilities present in the database. The results are displayed in a table within your terminal. Each vulnerability includes its
CVE ID
, the name of the affected package, and its severity level. When the problem's been patched in a later release, you'll see that update's version number in the
FIXED-IN
 column. This helps you establish whether a vulnerability can be readily addressed with a simple package manager update. Grype can work with packages for
all the most popular
 Linux distributions. It also supports Ruby Gems, NPM and Yarn packages, Python Eggs, Wheels, and Poetry dependencies, and Java modules in JAR, WAR, EAR, JPI, and HPI formats.                         Scanning Filesystems
Grype can scan filesystem paths on your machine. This lets you discover vulnerabilities in source code repositories before you've built an image. To use this feature, specify a directory path with the
dir:
 scheme:
grype dir:/example-dir
Grype will look for compatible files nested under the given directory root. Each found file will be indexed and scanned for vulnerabilities.

### Chunk #3
Filesystem scans surface the same types of vulnerability as container image scans. The scan might take a couple of minutes to complete if you're working with a large directory tree.                         Filtering Vulnerabilities
Two filtering flags are supported to scope the report to just the vulnerabilities or resolution options you're interested in:
--only-fixed
 - Only show vulnerabilities that have been patched in a later release of the affected package. --fail-on high
 - Exit immediately with an error code when a
high
-level vulnerability is found. You can substitute any supported error level (critical, high, medium, or low) instead of
high
.                         Ignoring Vulnerabilities
Vulnerabilities can be ignored to hide false positives or issues you've decided not to address, perhaps because they're not relevant to your use of the package. To ignore a vulnerability, you need to create a custom Grype config file in YAML format. Add the vulnerability's CVE under the top-level
ignore
 field:
ignore:
 - vulnerability: CVE-2021-12345
Other fields
are supported too
, such as this variant to ignore all issues stemming from NPM packages:
ignore:
 - package:
 type: npm
Save your config file to
.grype.yaml
 or
.grype/config.yaml
 in your working directory.

### Chunk #4
It'll be used automatically next time you run a Grype scan. The global config file
~/.grype.yaml
 is also supported. The file in your working directory will be merged with the global one at runtime. Vulnerabilities will not affect Grype's exit code if they're ignored. The JSON report will move them to a separate
ignoredMatches
 field while terminal table reports exclude them altogether. If you ignore a vulnerability, remember to document why it's been accepted so every contributor understands the risk.                         Using SBOMs
Grype can work with SBOMs generated
by Syft
, another of Anchore's projects. Syft indexes your container images to produce a list of the dependencies they contain. Use Syft to create an SBOM for your image in JSON format:
syft
alpine
:latest
-o
json
 >
alpine-sbom
.json
Then run a Grype scan using the SBOM:
grype sbom:/alpine-sbom.json
Grype will inspect the referenced image for new vulnerabilities arising from its bill of materials. Keep using Grype with your SBOM to monitor for emerging issues in image dependencies that you've already audited and indexed.

### Chunk #5
Customizing Grype Output
Grype provides four different output formatters which you can switch between using the
-o
 CLI flag:
table
 - The default human-readable table for in-terminal consumption. json
 - A JSON-formatted report containing much more comprehensive information about each vulnerability, as well as details of the Grype database used for scanning. JSON files are suitable for long-term archiving and comparison, or use as CI build artifacts. cyclonedx
 - A
CycloneDX-compatible report
 in XML format which is ready to feed into other tools supporting SBOMs and vulnerability lists. template
 - This advanced formatter lets you produce your own reports in arbitrary formats. The
template
 formatter accepts a Go template that will be used to render the report output. To use this formatter, don't specify it by name - instead, pass the path to a file containing your Go template:
grype
alpine
:latest
-o
output-template
.tmpl
The template should use the
Go templating syntax
 to reference variables that Grype provides. You can construct any kind of file format you need, such as an HTML page, a Markdown file, or a custom JSON structure. The Grype docs include
an example of
 producing a CSV file from the available variables.

### Chunk #6
Vulnerability Database
The vulnerability database stores details of all the vulnerabilities known to Grype. Once it's been downloaded, the cached version will be reused until an update is available. Manual interactions with the database aren't usually necessary. In some situations you might need to force a database download. This could be because you're setting up an air-gapped server in advance of running a scan. Use the
grype db check
 and
grype db update
 commands to check for and download a newer version of the database. Once the database is available, scans will work while your system's offline. You can disable Grype's automatic database update checks by setting the
GRYPE_DB_AUTO_UPDATE
 environment variable to
false
 in your shell.                         Summary
Grype alerts you to vulnerabilities inside your containers and on your filesystem. As a standalone CLI binary, it's easier to get started with than a full Anchore installation. If you're wondering which you should choose, Anchore's value lies in its extensibility and advanced configuration options. With Anchore Engine you can define your own policy sets based on gates, triggers, and actions. These let you precisely tailor your scans to your specific environment.

### Chunk #7
Grype provides a more streamlined experience when you just want a list of known vulnerabilities in your image. Whichever you choose, adopting some form of active vulnerability scanning will keep you informed of weaknesses in your
software supply chain
. For a fully integrated approach, use Grype as part of your CI pipeline so you're alerted to new vulnerabilities as code is committed. Programming
Web
Cybersecurity
                                            Follow
                                            Followed
                    Like
Share
Facebook
X
LinkedIn
Reddit
Flipboard
Copy link
Email
Readers like you help support How-To Geek. When you make a purchase using links on our site, we may earn an affiliate commission.
Read More
. Close
Recommended
			The NSA is Warning You to Restart your Phone Every Week: Here's Why
Cybersecurity
The NSA just warned you to restart your phone, and you should probably hear them out. Posts
13
Jul 15, 2024
			Why You Shouldn't Sign In With Google or Facebook
Cybersecurity
Signing in with your Google account has a few downsides.
Posts
20
Aug 19, 2024
			5 Python Easter Eggs That Make Learning Programming More Fun
Programming
Who thought programming languages could be funny?

### Chunk #8
Posts
5 days ago
			Nintendo Kicks off 6 Weeks of Goodies for Switch Online Subscribers
Video Games
On the eve of the Switch 2 release. Posts
2 days ago
			How to Use ChatGPT to Organize Your Bookmarks
Cutting Edge
Transform your messy bookmarks into an organized library with ChatGPT. Posts
2 days ago
			Google Wallet vs. Samsung Wallet: Which Should You Use? Android
It depends. What's in your wallet? Posts
11
4 days ago
                                                                    Desktop
                                                                    Mobile
			Apple Now Sells Refurbished M4 Macs at a Discount
12 hours ago
			5 Cheap Tech Accessories That Save My Sanity
13 hours ago
			This Rock Has an SSD in It
14 hours ago
See More
			Samsung Messages Just Got an Update, Even Though It’s Dead
14 hours ago
			Outlook Just Fixed My Biggest Issue With Mobile Email Apps
14 hours ago
See More
Join Our Team
Our Audience
About Us
Press & Events
Contact Us
Follow Us
Advertising
Careers
Terms
Privacy
Policies
How-To Geek
 is part of the
Valnet Publishing Group
                Copyright © 2025 Valnet Inc.

## Document: web-2

### Chunk #0
Grype Scanner: Complete Guide to Container Vulnerability Scans
                    Skip to main content
                            🏠  Home
                            🚀 Latest Blogs
                            👨‍💻 Courses
                            📩 Newsletter
                                    🏠  Home
                                    🚀 Latest Blogs
                                    👨‍💻 Courses
                                    📩 Newsletter
Quick search... ⌘K
/
                            🏠  Home
                            🚀 Latest Blogs
                            👨‍💻 Courses
                            📩 Newsletter
            Grype Scanner: Complete Guide to Container Vulnerability Scans
Learn how Grype Scanner secures containers with easy vulnerability scans
Nov 26, 2024
—
Aswin
Grype Scanner: Complete Guide to Container Vulnerability Scans
In this blog, we will look into the Grype vulnerability scanner. It is an open-source vulnerability scanner designed for container image.
Let's explore its features, benefits, installation, and usage. By the end of this blog, you'll learn:
What Grype is and how it works
Grype’s workflow for vulnerability scanning
How to scan container images for vulnerabilities using Grype
Configuring Grype for seamless integration into CI pipelines
Scanning Software Bill of Materials (SBOM) with Grype
Creating visually appealing HTML vulnerability reports
Lets get started. What is Grype? In the world of DevOps, keeping containerized applications secure is more important than ever. That’s where
Grype
 comes in. Grype is an open-source tool that helps you find vulnerabilities in container images and filesystems. It’s designed to catch security issues early and keep your applications safe.

### Chunk #1
What makes Grype special?
For one, it can scan container images stored in remote repositories without needing to download them. It can also analyze SBOM (Software Bill of Materials) files to check for vulnerabilities. Grype keeps its database updated automatically, using reliable sources like the National Vulnerability Database (NVD), Debian Security Tracker, Red Hat Security Advisories, and other trusted security lists. How to Install Grype? Run the following command to install Grype on your system. curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh | sh -s -- -b /usr/local/bin
This command downalod the Grype installation script and runs the script to install Grypt on the
/usr/local/bin
 directory. For Mac users,
brew tap anchore/grype
brew install grype
Once it is installed, run the following command to check if it's installed properly. grype version
If the installation is successful, this command shows the version of Grype installed in your system. Grype Scanner Workflow
The following image shows the high level workflow of Grype
Here’s how Grype works at a high level:
Grype maintains a local vulnerability database that is automatically updated.

### Chunk #2
The
.grype.yaml
 file can be used to set custom scanning rules, such as ignoring specific vulnerabilities or adjusting severity thresholds. Grype scans container images, filesystems, or SBOMs using its local database and the custom rules. It generates a report categorizing vulnerabilities by severity, type, and other configurable parameters. Scanning Vulnerability using Grype
Once the installation is complete, try to scan vulnerabilities. Grype can scan for vulnerabilities in Docker images, Filesystems, and even images in remote registry. Scan Docker Image using Grype
First, let's see how to scan a Docker image with Grype, run the following command to scan a Docker image for vulnerability. grype <image-name>
Grype scans your Docker image and give the output as shown below
You can see that it lists every vulnerability ID and severity. If you want to fail the scan if a specific vulnerability severity is in your image, run the following command. grype <image-name> --fail-on critical
This command scans if the Docker image has a vulnerability with the specified severity and fails the scan if present.

### Chunk #3
If the vulnerability with the specified severity is present, your scan will fail with the following message
discovered vulnerabilities at or above the severity threshold
Scan Docker Image in Remote Registry using Grype
Grype has the ability to scan for vulnerabilities in a Docker image in a remote registry, so you do not have to pull the image locally to scan the image. Run the following command to scan the
Docker image
 in a remote registry. grype registry:<image-name>
For example, to scan an image named
nginx
 in a remote registry:
grype registry:nginx:latest
Scan Filesystems using Grype
You can use Grype to scan vulnerabilities in the filesystem, this means Grype scans binaries, libraries, and other system files that are present in the specified directory for vulnerabilities. Run the following command to scan Filesystems. grype dir:<directory-path>
This command scans the specified directory and lists any vulnerabilities found in the system files. Custom Scanning Rules
Grype allows you to create custom scanning rules using a
.grype.yaml
 configuration file. These rules let you:
Ignore specific vulnerabilities. Adjust severity levels. Define custom output formats.

### Chunk #4
💡
Custom scanning rules are particulerly useful in
Image build CI pipelines
 where certain vulnerabilities may need to be temporarily suppressed or severity levels adjusted for specific use cases. Here’s an example
.grype.yaml
 file:
ignore:
  - vulnerability: CVE-2008-4318
    fix-state: unknown
    vex-status: not_affected
    vex-justification: vulnerable_code_not_present
    package:
      name: libcurl
      version: 1.5.1
      type: npm
      location: "/usr/local/lib/node_modules/**"
  - vulnerability: CVE-2014-54321
  - package:
      type: gem
To use this file, place it in the directory where you run Grype, or specify the file path with the
--config
 or
-c
 flag:
grype <image_name>:<tag> -c /<path>/.grype.yaml
Scan SBOMs with Grype
A Software Bill of Materials (SBOM) is a list of all the components, libraries, and dependencies used in a project.
SBOMs help identify potential vulnerabilities in software by showing all the underlying components in the software supply chain. Grype doesnt create SBOMs.
You can use tools like
Syft
  or Trivy to generate SBOM reports, Grype supports SPDX and CycloneDX SBOM formats.Grype can analyze SBOM generated from container images or filesystems to find vulnerabilities.

### Chunk #5
Run the following command to scan vulnerabilities using SBOM report
grype sbom:<sbom-report-name>
You will get an output as shown below
Get Output using Templates
Grype allows users to customize the report output using templates, which are helpful when integrating Grype with CI/CD pipelines. You can use custom templates to define how the vulnerability scan results are displayed. Grype allows HTML, CSV, and table formats by default, but you can also create your own custom templates as you like. You can get template files from the official
GitHub repo
. Download the template format you want and run the following command to get the output using the template formate. For example, let's say you want the scan output format in HTML, download the HTML template, and run the following command
grype <image-name> -o template -t html.tmpl > report.html
I have used the
nginx:latest
 image to get the output in HTML format, got the output as shown below when running the output HTML file
Conclusion
If you look at the
4Cs of cloud-native security
, container security plays a key role. Grype is a versatile tool for vulnerability scanning in containerized applications.

### Chunk #6
Whether you're scanning
Docker images
, filesystems, or SBOMs, Grype helps secure your applications with ease. With its automatic updates, remote scanning capabilities, and custom configurations, it’s an essential addition to any DevOps security toolkit. Now that you’ve learned about Grype, here are a few questions for you:
Have you tried using Grype in your projects? If yes, what was your experience? What other tools do you use for vulnerability scanning, and how do they compare to Grype? Do you see Grype fitting into your CI/CD pipeline, and if so, how would you implement it? Are there specific challenges you’ve faced with container security that a tool like Grype might solve? I’d love to hear your thoughts and experiences in the comments! Your feedback and ideas could spark great discussions and help others in the community.                     Aswin
Aswin Vijayan is a DevOps engineer with a passion for open-source tools and automation. In his free time, Aswin enjoys reading and exploring new technologies.                                 Website
                                India
                             Blog that covers DevOps, Kuebrnetes MLOps, CI/CD, DevSecOps and much more
                                Subscribe to our newsletter
                                Get the latest posts and updates delivered to your inbox.
 No spam. Unsubscribe anytime.

### Chunk #7
Enter your email
                                Subscribe
                    ⚙️ Jenkins Course
Techiescamp
 © 2025
•
                        Published with
Ghost
 and
Spiritix
