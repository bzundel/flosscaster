require 'rss'
require 'open-uri'

def create_rss_feed(title, link, description, items)
  RSS::Maker.make("2.0") do |maker|
    maker.channel.title = title
    maker.channel.link = link
    maker.channel.description = description

    items.each do |item|
      maker.items.new_item do |new_item|
        new_item.title = item[:title]
        new_item.link = item[:link]
        new_item.description = item[:description]
        new_item.enclosure.url = item[:enclosure_url]
        new_item.enclosure.length = item[:enclosure_length]
        new_item.enclosure.type = item[:enclosure_type]
      end
    end
  end
end

def load_existing_feed(file_path)
  RSS::Parser.parse(File.read(file_path), false)
end

def save_rss_feed(file_path, rss_content)
  File.open(file_path, 'w') do |file|
    file.write(rss_content)
  end
end

def main
  if ARGV.length < 5
    puts "Usage: ruby rss_generator.rb <title> <link> <description> <item1_title,item1_link,item1_description,item1_enclosure_url,item1_enclosure_length,item1_enclosure_type> [<item2_title,item2_link,item2_description,item2_enclosure_url,item2_enclosure_length,item2_enclosure_type> ...]"
    exit
  end

  title = ARGV[0]
  link = ARGV[1]
  description = ARGV[2]
  items = ARGV[3..-1].map do |arg|
    item_parts = arg.split(',')
    {
      title: item_parts[0],
      link: item_parts[1],
      description: item_parts[2],
      enclosure_url: item_parts[3],
      enclosure_length: item_parts[4].to_i,
      enclosure_type: item_parts[5]
    }
  end

  file_path = 'feed.xml'

  if File.exist?(file_path)
    puts "RSS feed exists. Loading existing feed..."
    existing_feed = load_existing_feed(file_path)

    # Füge neue Artikel zum bestehenden Feed hinzu
    items.each do |item|
      existing_feed.items.new_item do |new_item|
        new_item.title = item[:title]
        new_item.link = item[:link]
        new_item.description = item[:description]
        new_item.enclosure.url = item[:enclosure_url]
        new_item.enclosure.length = item[:enclosure_length]
        new_item.enclosure.type = item[:enclosure_type]
      end
    end

    save_rss_feed(file_path, existing_feed.to_s)
    puts "Neue Artikel wurden zum bestehenden RSS-Feed hinzugefügt."
  else
    rss_content = create_rss_feed(title, link, description, items)
    save_rss_feed(file_path, rss_content)
    puts "Neuer RSS-Feed erstellt und in #{file_path} gespeichert."
  end
end

main

