provider "aws" {
	region = "eu-central-1"
}

resource "aws_lightsail_static_ip" "bot_ip" {
  name = "bot_ip"
}

resource "aws_lightsail_static_ip_attachment" "bot_ip_attachment" {
  static_ip_name = aws_lightsail_static_ip.bot_ip.name
  instance_name = aws_lightsail_instance.botbase.name
}

resource "aws_lightsail_instance" "botbase" {
  name = "botbase"
  availability_zone = "eu-central-1a"
  blueprint_id = "ubuntu_20_04"
  bundle_id = "nano_1_0"
  user_data = file("botbase.sh")
}
