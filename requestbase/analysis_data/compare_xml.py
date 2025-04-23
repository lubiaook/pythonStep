from lxml import etree as ET


def compare_elements(elem1, elem2):
    differences = []

    # 比较属性
    attrs1 = elem1.attrib
    attrs2 = elem2.attrib

    for attr in attrs1:
        if attr not in attrs2:
            differences.append(f"Attribute '{attr}' missing in second element")
        elif attrs1[attr] != attrs2[attr]:
            differences.append(f"Different values for attribute '{attr}': '{attrs1[attr]}' != '{attrs2[attr]}'")

    for attr in attrs2:
        if attr not in attrs1:
            differences.append(f"Attribute '{attr}' missing in first element")

    return differences


def compare_trees(tree1, tree2):
    differences = []

    root1 = tree1.getroot()
    root2 = tree2.getroot()

    # 遍历root2的所有元素，并在root1中查找对应的元素
    for elem2 in root2.iter():
        xpath = tree2.getpath(elem2)
        elem1 = root1.xpath(xpath)
        if not elem1:
            differences.append(f"Element '{xpath}' missing in first XML")
        else:
            elem1 = elem1[0]
            element_diffs = compare_elements(elem1, elem2)
            if element_diffs:
                differences.append(f"Differences in element '{xpath}': {element_diffs}")

    return differences


if __name__ == '__main__':
    # 读取文件1和文件2的内容
    with open('prod.xml', 'r', encoding='utf8') as f1, open('local.xml', 'r', encoding='utf8') as f2:
        xml1 = f1.read()
        xml2 = f2.read()

    # 解析XML
    tree1 = ET.ElementTree(ET.fromstring(xml1.encode()))
    tree2 = ET.ElementTree(ET.fromstring(xml2.encode()))

    differences = compare_trees(tree1, tree2)

    print("Differences found:")
    for diff in differences:
        print(diff)
