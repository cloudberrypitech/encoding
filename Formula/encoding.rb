class Encoding < Formula
  desc "Simple Base64 file encoding and decoding CLI"
  homepage "https://github.com/cloudberrypitech/encoding"
  url "https://github.com/cloudberrypitech/encoding/releases/download/v1.0.0/encoding-1.0.0.tar.gz"
  sha256 "b4f0feadca4e5ff128a2c965574f28961627fd71fb0370111c77d0e46406036f"
  license "MIT"

  depends_on "python@3.14"

  def install
    virtualenv_create(libexec, "python3.14")
    system libexec/"bin/pip", "install", "--no-deps", buildpath
    bin.install_symlink libexec/"bin/encoding"
  end

  test do
    (testpath/"input.txt").write "hello"
    system bin/"encoding", "encode", testpath/"input.txt"
    assert_equal "aGVsbG8=", (testpath/"input.txt.b64").read
  end
end
