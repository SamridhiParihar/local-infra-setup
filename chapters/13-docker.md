# Chapter 13 — Docker

## 1. What Docker is for

Docker packages an app with the files and software it needs to run. This helps the same app run in a more consistent way on different computers.

For example, a local AI app might need Python, certain libraries, and a particular runtime. A Docker image can package those pieces so you do not have to install each one directly into macOS.

## 2. Image and container

- An **image** is the packaged template: it includes files, libraries, and settings needed to run an app.
- A **container** is a running instance made from that image.

You can create multiple containers from the same image. The image acts like a template; each container runs as its own isolated process. [Docker: What is an image?](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-an-image/), [Docker: What is a container?](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/)

## 3. Dockerfile: the recipe for an image

A **Dockerfile** is a set of instructions for building an image. It might say:

1. Start from an image that includes Python.
2. Copy in the app's code.
3. Install the app's libraries.
4. Set the command that starts the app.

You can then build an image from that recipe and run containers from it.

## 4. Containers versus virtual machines

A virtual machine, such as one you run in UTM, acts like a separate computer with its own operating system. A container is an isolated app process that shares a system kernel with other containers.

On a Mac, Docker Desktop runs Linux containers inside a lightweight Linux virtual machine, because macOS does not provide the Linux kernel those containers need. So Docker containers are not full VMs, but Docker Desktop still uses a VM behind the scenes. [Docker: Containers versus VMs](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/), [Docker Desktop for Mac FAQ](https://docs.docker.com/desktop/troubleshoot-and-support/faqs/macfaqs/)

That VM uses some of the Mac's resources. Docker Desktop lets you manage its settings, including how much memory and CPU it can use.

## 5. Container files and persistent data

A container has its own file area. By default, changes written inside a container are tied to that container. If you remove the container, those changes may be removed too.

To keep data beyond the container's lifetime, Docker provides:

- **Volumes:** storage managed by Docker and kept separately from a container.
- **Bind mounts:** folders or files from your computer made available inside a container.

For an AI app, model weights and experiment results often belong in a volume or a bind mount, rather than being built into the image. This helps keep large model files separate from the app package. [Docker storage documentation](https://docs.docker.com/engine/storage/)

## 6. Ports: connecting to an app in a container

A container's app is isolated from your Mac by default. **Port publishing** forwards a port on the Mac to a port inside the container.

For example:

```text
Mac port 8080 → container port 80
```

Then an app in the container listening on port `80` can be reached from the Mac using port `8080`. Docker's port documentation describes this as a forwarding rule. [Docker: Publishing ports](https://docs.docker.com/get-started/docker-concepts/running-containers/publishing-ports/)

## 7. Docker Compose

A project may use several containers together—for example:

- One container for a Python app
- One for a database
- One for a model-serving runtime

**Docker Compose** lets you describe that group in a `compose.yaml` file and manage the services together. This is useful when an AI project has more than one service. [Docker Compose quickstart](https://docs.docker.com/compose/gettingstarted/)

## 8. How Docker fits into local AI

A possible local AI setup could look like this:

```text
Your Python app container
        ↓ sends a request
Model runtime container
        ↓ uses
Model files in a mounted volume
```

Docker helps package and run the app or runtime. It does not create a model or make the computer's hardware more powerful. Access to GPU acceleration depends on the computer and the particular Docker/runtime setup.

## Key takeaways

- An image is a packaged template; a container is a running instance of it.
- A Dockerfile describes how to build an image.
- Containers are isolated processes, not full virtual machines.
- Docker Desktop on Mac uses a Linux VM to run Linux containers, so it uses some Mac resources.
- Use volumes or bind mounts for data you want to keep, such as model files and experiment results.
- Publish a port when you need to reach an app inside a container.
- Docker Compose coordinates projects that use multiple containers.

## References

- [Docker: What is an image?](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-an-image/)
- [Docker: What is a container?](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/)
- [Docker Desktop for Mac FAQ](https://docs.docker.com/desktop/troubleshoot-and-support/faqs/macfaqs/)
- [Docker storage documentation](https://docs.docker.com/engine/storage/)
- [Docker: Publishing ports](https://docs.docker.com/get-started/docker-concepts/running-containers/publishing-ports/)
- [Docker Compose quickstart](https://docs.docker.com/compose/gettingstarted/)
